import smtplib
import email.utils
from email.mime.text import MIMEText
from concurrent import futures
from logger import TimedRotatingFileErrorLogger
import traceback
import time


LOGGER = TimedRotatingFileErrorLogger('mail_receiver_test', 'mail_receiver_test.log', logging_level='INFO')

TEST_EMAILS = {
    'VW_NY_NewYork_WashingtonHeights@mail.fsgenergy.com': (
        '''Fri Jul 10 14:18:17 2015

An EMS Notification Has Occurred

EMS Point: RTU 2 Fan Status
EMS Value: On
EMS Message: Fan Alarm-The Supply Fan Has Failed to Stop.'''
    ),

    'VW_CA_CorteMadera@mail.fsgenergy.com': (
        '''Fri Jul 10 11:06:37 2015

An EMS Return To Normal Has Occurred

EMS Point: RTU 1 Filter
EMS Value: Clean
EMS Message: Filter Alert-The Air Filter is Clean.'''
    ),

    'VW_KY_Lexington-Nicholasville@mail.fsgenergy.com': (
        '''Fri Jul 10 13:36:51 2015

An EMS Notification Has Occurred

EMS Point: RTU 2 Fan Status
EMS Value: Off
EMS Message: Fan Alarm-The Supply Fan Has Failed to Start.'''
    ),

    'VW_KS_Topeka@mail.fsgenergy.com': (
        '''Fri Jul 10 12:23:51 2015

An EMS Notification Has Occurred

EMS Point: RTU 3 IN-05 Comp 1 High Pressure Temp
EMS Value: -327 Deg.F.
EMS Message: Sensor Alert-Sensor has Failed.'''
    ),

    'VW_AZ_Chandler_ChandlerVillage@mail.fsgenergy.com': (
        '''Fri Jul 10 10:34:45 2015

An EMS Notification Has Occurred

EMS Point: RTU 6 Filter
EMS Value: Dirty
EMS Message: Filter Alert-The Air Filter is Dirty.'''
    )
}

EMAIL_SUBJECTS = {
    'VW_NY_NewYork_WashingtonHeights@mail.fsgenergy.com':
        '[vzw-alarms:3496290] VW_NY_NewYork_WashingtonHeights: Alarm Active - Alarm RTU Fan Stop',
    'VW_CA_CorteMadera@mail.fsgenergy.com':
        '[vzw-alarms:3496246] VW_CA_CorteMadera: Alarm Cleared - Alert RTU Filter Pressure Drop',
    'VW_KY_Lexington-Nicholasville@mail.fsgenergy.com':
        '[vzw-alarms:3496181] VW_KY_Lexington_Nicholasville: Alarm Active - Alarm RTU Fan Start',
    'VW_KS_Topeka@mail.fsgenergy.com':
        '[vzw-alarms:3496141] VW_KS_Topeka: Alarm Active - Alert SensorFault C1HPT',
    'VW_AZ_Chandler_ChandlerVillage@mail.fsgenergy.com':
        '[vzw-alarms:3496142] VW_AZ_Chandler_ChandlerVillage: Alarm Active - Alert RTU Filter Pressure Drop'
}


def test_receiver():
    msgs = {}
    for sr in TEST_EMAILS.keys():
        current_msg = MIMEText(TEST_EMAILS[sr])
        current_msg['To'] = current_msg['From'] = email.utils.formataddr((sr.split('@')[0], sr))
        current_msg['Subject'] = EMAIL_SUBJECTS[sr]
        msgs[sr] = current_msg

    server = smtplib.SMTP('130.211.182.211', 8888)
    i = 0
    while i < 20:
        for sr in msgs:
            try:
                server.sendmail(sr, [sr], msgs[sr].as_string())
                LOGGER.send_error('message sent at ts {}'.format(time.time()), msgs[sr].as_string(), log_level='INFO')
            except:
                LOGGER.send_error(traceback.format_exc())
        i += 1

    return 'sent all messages'


def multiple_thread_test_receiver():
    with futures.ThreadPoolExecutor(25) as ex:
        upcoming_futures = []

        for i in range(50):
            upcoming_futures.append(ex.submit(test_receiver))

        for f in futures.as_completed(upcoming_futures):
            try:
                LOGGER.send_error(f.result(), log_level='INFO')
            except:
                LOGGER.send_error(traceback.format_exc())

    return 'threads complete'


if __name__ == '__main__':
    with futures.ProcessPoolExecutor() as ex:
        upcoming_futures = []

        for i in range(20):
            upcoming_futures.append(ex.submit(test_receiver))

        for f in futures.as_completed(upcoming_futures):
            try:
                LOGGER.send_error(f.result(), log_level='INFO')
            except:
                LOGGER.send_error(traceback.format_exc())
