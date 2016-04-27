from simple_mail_server import SimpleMailServer
from sqlalchemy import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm import sessionmaker
from logger import TimedRotatingFileErrorLogger
from mail_orm import Base

import argparse
import asyncore
import yaml
import getpass


def start_server(ip_address, port, connection_string, logger, msg_ttl):
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    server = SimpleMailServer((ip_address, port), None, session=scoped_session(sessionmaker(bind=engine)),
                              connection_string=connection_string, logger=logger, msg_ttl=msg_ttl)
    asyncore.loop()


def prompt_for_password(prompt, second_prompt):
    test_pass = ''
    test_pass_2 = ' '
    while test_pass != test_pass_2:
        test_pass = getpass.getpass(prompt)
        test_pass_2 = getpass.getpass(second_prompt)
        if test_pass != test_pass_2:
            print 'Passwords do not match. Try again.'
    return test_pass


def prompt_for_username(prompt):
    test_un = raw_input(prompt)
    while not test_un:
        print 'Username must be provided. Try again.'
        test_un = raw_input(prompt)
    return test_un


def parse_arguments(args_to_parse=None):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('config_file', metavar='configuration_file',
                                 help='YAML file containing required configuration information')
    argument_parser.add_argument('-u', '--db_username', help='Username for the database configured in the YAML file',
                                 dest='db_username', default=None)
    argument_parser.add_argument('-p', '--db_password', help='Password corresponding to the database username',
                                 dest='db_password', default=None)

    current_args = argument_parser.parse_args(args_to_parse)
    with open(current_args.config_file) as f:
        config_dict = yaml.safe_load(f)

    if 'db_username' not in config_dict:
        config_dict['db_username'] = current_args.db_username or prompt_for_username('Database Username: ')
        config_dict['db_password'] = current_args.db_password or prompt_for_password('Database Password: ',
                                                                                     'Reenter Database Password: ')

    if 'connection_string' not in config_dict:
        config_dict['connection_string'] = ('{}://{}:{}@{}:{}/{}'
                                            .format(config_dict['db_protocol'], config_dict['db_username'],
                                                    config_dict['db_password'], config_dict['db_host'],
                                                    config_dict['db_port'], config_dict['db_name']))

    return (config_dict['ip_address'], int(config_dict['port']), config_dict['connection_string'],
            TimedRotatingFileErrorLogger(config_dict['log_name'], config_dict['log_location']),
            config_dict['msg_ttl'])


if __name__ == '__main__':
    start_server(*(parse_arguments()))
