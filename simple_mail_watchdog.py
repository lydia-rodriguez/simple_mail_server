import os
import time
import argparse
import traceback

from logger import TimedRotatingFileErrorLogger
from logging import handlers

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


MESSAGE_DIFFERENCE_TIME = 180
MESSAGE_MISSED_CHECK = False


def main(py_loc, proc_loc, log_file, config_file):
    proc = None
    py_loc = os.path.abspath(py_loc)
    proc_loc = os.path.abspath(proc_loc)
    config_file = os.path.abspath(config_file)
    logger = TimedRotatingFileErrorLogger('mail_watchdog_log', log_file)
    # logger.underlying_log.addHandler(handlers.SMTPHandler())
    f = open(os.path.join(proc_loc, 'message_parsed_file'), 'w')
    f.close()
    try:
        while True:
            if proc is None:
                print('starting process')
                proc = subprocess.Popen([
                    py_loc,
                    os.path.join(proc_loc, 'start_server.py'),
                    config_file
                ])

            if proc.poll() is None:
                # print 'sleep for {}'.format(MESSAGE_DIFFERENCE_TIME)
                i = 0
                while proc.poll() is None and i < MESSAGE_DIFFERENCE_TIME:
                    time.sleep(1)
                    i += 1
                # print 'sleep complete'

            last_message_time = os.stat(os.path.join(proc_loc, 'message_parsed_file')).st_mtime
            if last_message_time <= time.time() - MESSAGE_DIFFERENCE_TIME:
                logger.send_error('Last message received at {}. Restarting service if option enabled.'.format(last_message_time))
                if MESSAGE_MISSED_CHECK:
                    print('killing process')
                    try:
                        proc.kill()
                    except:
                        logger.send_error(traceback.format_exc())

            if proc.poll() is not None:
                proc = None

    except KeyboardInterrupt:
        if proc:
            proc.kill()
        raise


def parse_arguments():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-p', '--py_loc', help='Location of the Python executable',
                                 default='/usr/bin/python')
    argument_parser.add_argument('-r', '--proc_loc', help='directory containing start_server.py',
                                 default='/opt/mail-server')
    argument_parser.add_argument('-l', '--log_file', help='location of configuration file for start_server.py',
                                 default='/var/log/mail_parser/mail_watchdog.log')
    argument_parser.add_argument('-c', '--config_file', help='location of configuration file for start_server.py',
                                 default='/opt/mail-server/mail_server_config.yaml')

    return argument_parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.py_loc, args.proc_loc, args.log_file, args.config_file)
