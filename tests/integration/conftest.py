import os

import pytest


@pytest.fixture(scope='session')
def get_token() -> str:
    token = os.getenv('EASY_NOTIFYER_TELEGRAM_TOKEN')
    if token is not None:
        return token
    raise ValueError("TOKEN IS NOT FOUND")


@pytest.fixture(scope='session')
def get_chat_id() -> int:
    chat_id = os.getenv('EASY_NOTIFYER_TELEGRAM_CHAT_ID')
    if chat_id is not None:
        return int(chat_id)
    raise ValueError("CHAT ID IS NOT FOUND")
