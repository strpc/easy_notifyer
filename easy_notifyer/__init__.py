from easy_notifyer.handlers import mailer_reporter, telegram_reporter
from easy_notifyer.mailer import Mailer
from easy_notifyer.telegram import Telegram


__version__ = '0.0.4'


__all__ = [
    "Mailer",
    "Telegram",
    "mailer_reporter",
    "telegram_reporter",
]
