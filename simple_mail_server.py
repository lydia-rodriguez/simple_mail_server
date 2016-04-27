from mail_orm import Message
from pm_hook import process_message_hook
from sqlalchemy import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm import sessionmaker
import smtpd
import traceback
import time


class SimpleMailServer(smtpd.SMTPServer):
    def __init__(self, *args, **kwargs):
        self._message_retry_count = 0
        self._conn_str = kwargs['connection_string']
        self._session = kwargs['session']
        self._logger = kwargs['logger']
        self._message_ttl = kwargs.get('msg_ttl', 9999999999)
        self._message_ttl_enabled = kwargs.get('msg_ttl_enabled', False)
        kwargs.pop('session', None)
        kwargs.pop('logger', None)
        kwargs.pop('msg_ttl', None)
        kwargs.pop('connection_string', None)
        smtpd.SMTPServer.__init__(self, *args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            # print data
            time_received = time.time()
            ttl_ts = time_received + self._message_ttl
            self._session.add(Message(source=str(peer), sender=str(mailfrom), recipients=str(rcpttos), body=str(data),
                                      time_received=time_received, ttl_ts=ttl_ts))
            process_message_hook(peer, mailfrom, rcpttos, data)
            if self._message_ttl_enabled:
                self._session.query(Message).filter(Message.ttl_ts <= time.time()).delete()
            self._session.commit()
            self._message_retry_count = 0
            with open('message_parsed_file', 'w') as f:
                f.write(str(time_received))
        except:
            self._session.rollback()
            self._message_retry_count += 1
            if self._message_retry_count > 4:
                self._logger.send_error(traceback.format_exc())
                self._session = scoped_session(sessionmaker(bind=create_engine(self._conn_str)))
            if self._message_retry_count > 5:
                raise
            self.process_message(peer, mailfrom, rcpttos, data)
