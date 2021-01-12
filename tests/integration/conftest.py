import os
import typing as t

import pytest

from easy_notifyer import Telegram


@pytest.fixture(scope='function')
def get_token() -> str:
    token = os.getenv('EASY_NOTIFYER_TELEGRAM_TOKEN')
    if token is not None:
        return token
    raise ValueError("TOKEN IS NOT FOUND")


@pytest.fixture(scope='function')
def set_token(get_token: str):
    os.environ.setdefault('EASY_NOTIFYER_TELEGRAM_TOKEN', get_token)


@pytest.fixture(scope='function')
def get_row_chat_ids() -> str:
    return os.getenv('EASY_NOTIFYER_TELEGRAM_CHAT_ID')


@pytest.fixture(scope='function')
def get_chat_id(get_row_chat_ids) -> t.List[int]:
    if get_row_chat_ids is not None:
        chat_id = [i.strip() for i in get_row_chat_ids.split(',')]
        chat_id = [int(i) for i in chat_id if i]
        return chat_id
    raise ValueError("CHAT ID IS NOT FOUND")


@pytest.fixture(scope='function')
def set_chat_id(get_chat_id: str):
    os.environ.setdefault('EASY_NOTIFYER_TELEGRAM_CHAT_ID', get_chat_id)


@pytest.fixture(scope='function')
def ready_client(get_token: str, get_chat_id: t.List[int]):
    return Telegram(token=get_token, chat_id=get_chat_id)


@pytest.fixture(scope='function')
def disable_notification_params() -> t.Dict:
    return {'disable_notification': True}


@pytest.fixture(scope='function')
def disable_web_page_preview_params() -> t.Dict:
    return {'disable_web_page_preview': True}
