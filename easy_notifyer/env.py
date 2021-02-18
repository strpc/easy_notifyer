# pylint: disable=invalid-name, invalid-envvar-default
import os


__all__ = [
    'Env',
]


class Env:
    def __init__(self):
        self.EASY_NOTIFYER_SERVICE_NAME = os.getenv('EASY_NOTIFYER_SERVICE_NAME')
        self.EASY_NOTIFYER_DATE_FORMAT = os.getenv('EASY_NOTIFYER_DATE_FORMAT', '%Y-%m-%d %H:%M:%S')
        self.EASY_NOTIFYER_FILENAME_DT_FORMAT = os.getenv(
            'EASY_NOTIFYER_FILENAME_DT_FORMAT', '%Y-%m-%d %H_%M_%S'
        )
        self.EASY_NOTIFYER_TELEGRAM_TOKEN = os.getenv('EASY_NOTIFYER_TELEGRAM_TOKEN')
        self.EASY_NOTIFYER_TELEGRAM_CHAT_ID = os.getenv('EASY_NOTIFYER_TELEGRAM_CHAT_ID')
        self.EASY_NOTIFYER_TELEGRAM_API_URL = os.getenv(
            'EASY_NOTIFYER_TELEGRAM_API_URL', 'https://api.telegram.org/'
        )
        self.EASY_NOTIFYER_MAILER_HOST = os.getenv('EASY_NOTIFYER_MAILER_HOST')
        self.EASY_NOTIFYER_MAILER_PORT = os.getenv('EASY_NOTIFYER_MAILER_PORT')
        self.EASY_NOTIFYER_MAILER_LOGIN = os.getenv('EASY_NOTIFYER_MAILER_LOGIN')
        self.EASY_NOTIFYER_MAILER_PASSWORD = os.getenv('EASY_NOTIFYER_MAILER_PASSWORD')
        self.EASY_NOTIFYER_MAILER_FROM = os.getenv('EASY_NOTIFYER_MAILER_FROM')
        self.EASY_NOTIFYER_MAILER_TO = os.getenv('EASY_NOTIFYER_MAILER_TO')
        self.EASY_NOTIFYER_MAILER_SSL = os.getenv(
            'EASY_NOTIFYER_MAILER_SSL', False) in (True, 'True'
                                                   )
