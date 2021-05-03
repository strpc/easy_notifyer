# pylint: disable=invalid-name, invalid-envvar-default
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ReportConfig:
    service_name: Optional[str]
    date_format: Optional[str]
    filename_dt_format: Optional[str]


@dataclass
class TelegramConfig:
    token: Optional[str]
    chat_id: Optional[str]
    api_url: Optional[str]


@dataclass
class MailerConfig:
    host: Optional[str]
    port: Optional[int]
    login: Optional[str]
    password: Optional[str]
    from_addr: Optional[List[str]]
    to_addrs: Optional[List[str]]
    ssl: Optional[bool]


@dataclass
class Config:
    report: ReportConfig
    telegram: TelegramConfig
    mailer: MailerConfig


def get_config() -> Config:
    report_config = ReportConfig(
        service_name=os.getenv("EASY_NOTIFYER_SERVICE_NAME"),
        date_format=os.getenv("EASY_NOTIFYER_DATE_FORMAT",
                              "%Y-%m-%d %H:%M:%S"),
        filename_dt_format=os.getenv("EASY_NOTIFYER_FILENAME_DT_FORMAT",
                                     "%Y-%m-%d %H_%M_%S"),
    )
    telegram_config = TelegramConfig(
        token=os.getenv("EASY_NOTIFYER_TELEGRAM_TOKEN"),
        chat_id=os.getenv("EASY_NOTIFYER_TELEGRAM_CHAT_ID"),
        api_url=os.getenv("EASY_NOTIFYER_TELEGRAM_API_URL"),
    )
    mailer_config = MailerConfig(
        host=os.getenv("EASY_NOTIFYER_MAILER_HOST"),
        port=os.getenv("EASY_NOTIFYER_MAILER_PORT"),
        login=os.getenv("EASY_NOTIFYER_MAILER_LOGIN"),
        password=os.getenv("EASY_NOTIFYER_MAILER_PASSWORD"),
        from_addr=os.getenv("EASY_NOTIFYER_MAILER_FROM"),
        to_addrs=os.getenv("EASY_NOTIFYER_MAILER_TO"),
        ssl=os.getenv("EASY_NOTIFYER_MAILER_SSL", False) in (True, "True"),
    )
    config = Config(report=report_config,
                    telegram=telegram_config,
                    mailer=mailer_config)
    return config
