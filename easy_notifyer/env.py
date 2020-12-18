import os
from dataclasses import dataclass


@dataclass
class Env:
    EASY_NOTIFYER_TELEGRAM_TOKEN: str = os.getenv('EASY_NOTIFYER_TELEGRAM_TOKEN')
    EASY_NOTIFYER_TELEGRAM_CHAT_ID: str = os.getenv('EASY_NOTIFYER_TELEGRAM_CHAT_ID')
    EASY_NOTIFYER_PROJECT_NAME: str = os.getenv('EASY_NOTIFYER_PROJECT_NAME')
    EASY_NOTIFYER_DATE_FORMAT: str = os.getenv('EASY_NOTIFYER_DATE_FORMAT',
                                               '%Y-%m-%d %H:%M:%S')
    EASY_NOTIFYER_FILENAME_DT_FORMAT: str = os.getenv('EASY_NOTIFYER_FILENAME_DT_FORMAT',
                                                   '%Y-%m-%d %H_%M_%S')
    EASY_NOTIFYER_API_BASE_URL: str = os.getenv('EASY_NOTIFYER_API_BASE_URL',
                                                'https://api.telegram.org/')
