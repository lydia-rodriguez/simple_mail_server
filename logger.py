import logging
from logging import handlers
import time


class TimedRotatingFileErrorLogger(object):
    def __init__(self, log_name, log_location, number_of_backups=20, when_value='W6',
                 logging_level='WARNING'):
        logging_level = getattr(logging, logging_level)
        log = logging.getLogger(log_name)
        log.setLevel(logging_level)
        handler = handlers.TimedRotatingFileHandler(log_location, when=when_value, interval=1, utc=True,
                                                    backupCount=number_of_backups)
        formatter = logging.Formatter('"%(asctime)s","%(levelname)s",%(message)s')
        formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        log.addHandler(handler)
        self._log = log

    def send_error(self, *args, **kwargs):
        log_level = getattr(logging, kwargs.get('log_level', 'WARNING'))
        error_tuple = (error_msg.replace('"', '""') for error_msg in args)
        self._log.log(log_level, ','.join('"{}"'.format(msg) for msg in error_tuple))

    @property
    def underlying_log(self):
        return self._log
