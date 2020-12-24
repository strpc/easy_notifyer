# pylint: disable=invalid-name, invalid-envvar-default
import os
from dataclasses import dataclass


__all__ = [
    'Env',
]


@dataclass
class EnvTelegram:
    """Enironment variables of telegram"""
    EASY_NOTIFYER_PROJECT_NAME: str = os.getenv('EASY_NOTIFYER_PROJECT_NAME')
    EASY_NOTIFYER_DATE_FORMAT: str = os.getenv('EASY_NOTIFYER_DATE_FORMAT',
                                               '%Y-%m-%d %H:%M:%S')
    EASY_NOTIFYER_FILENAME_DT_FORMAT: str = os.getenv('EASY_NOTIFYER_FILENAME_DT_FORMAT',
                                                      '%Y-%m-%d %H_%M_%S')
    EASY_NOTIFYER_TELEGRAM_TOKEN: str = os.getenv('EASY_NOTIFYER_TELEGRAM_TOKEN')
    EASY_NOTIFYER_TELEGRAM_CHAT_ID: str = os.getenv('EASY_NOTIFYER_TELEGRAM_CHAT_ID')
    EASY_NOTIFYER_TELEGRAM_API_URL: str = os.getenv('EASY_NOTIFYER_TELEGRAM_API_URL',
                                                    'https://api.telegram.org/')


@dataclass
class EnvMailer:
    """Enironment variables of mailer"""
    EASY_NOTIFYER_MAILER_HOST: str = os.getenv('EASY_NOTIFYER_MAILER_HOST')
    EASY_NOTIFYER_MAILER_PORT: str = os.getenv('EASY_NOTIFYER_MAILER_PORT')
    EASY_NOTIFYER_MAILER_LOGIN: str = os.getenv('EASY_NOTIFYER_MAILER_LOGIN')
    EASY_NOTIFYER_MAILER_PASSWORD: str = os.getenv('EASY_NOTIFYER_MAILER_PASSWORD')
    EASY_NOTIFYER_MAILER_FROM: str = os.getenv('EASY_NOTIFYER_MAILER_FROM')
    EASY_NOTIFYER_MAILER_TO: str = os.getenv('EASY_NOTIFYER_MAILER_TO')
    EASY_NOTIFYER_MAILER_SSL: bool = os.getenv('EASY_NOTIFYER_MAILER_SSL', False) in (True, 'True')


@dataclass
class Env(EnvTelegram, EnvMailer):
    """Hub enironment variables"""
