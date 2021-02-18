import os
import inspect
import typing as t

import pytest

from easy_notifyer import Telegram
from easy_notifyer.exceptions import ConfigError


def test_send_message(get_token: str, get_chat_id: int):
    """Базовая отправка сообщения"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f"test base send_message. with link preview https://github.com {test_name}"

    client = Telegram(token=get_token, chat_id=get_chat_id)
    result = client.send_message(msg)

    assert result is True


@pytest.mark.parametrize('token,chat_id', [
    ('qweqweqwe', 123123123),
    ('foobar', 00000000),
])
def test_send_message_exception(token: str, chat_id: int):
    """Проверка ошибки при отправке базового сообщения при невалидных чатайди"""
    client = Telegram(token=token, chat_id=chat_id)
    with pytest.raises(ConfigError):
        _ = client.send_message('')


def test_send_message_two_chat_ids(get_token: str, get_chat_id: int):
    """Отправка базового сообщения в два чата"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'test two chat_ids(2 msg to one chat id) send message. {test_name}'

    two_tokens = [get_chat_id, get_chat_id]
    client = Telegram(token=get_token, chat_id=two_tokens)
    result = client.send_message(msg)

    assert result is True


@pytest.mark.parametrize('token,chat_id', [
    ('qweqweqwe', 123123123),
    ('foobar', 00000000),
])
def test_send_message_two_chat_ids_exception(token: str, chat_id: int):
    """Проверка ошибки при отправке базового сообщения в два чата"""
    client = Telegram(token=token, chat_id=chat_id)
    with pytest.raises(ConfigError):
        _ = client.send_message('msg')


@pytest.mark.parametrize('param', [
    {'disable_web_page_preview': True},
    {'disable_notification': True},
    {'disable_web_page_preview': True, 'disable_notification': True},
])
def test_send_message_with_params(get_token: str, get_chat_id: int, param: t.Dict):
    """Отправка сообщения с параметрами"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'{param=}\ntest send message with param.\n{test_name} https://github.com/'

    client = Telegram(token=get_token, chat_id=get_chat_id)
    result = client.send_message(msg, **param)

    assert result is True


@pytest.mark.parametrize('param', [
    {'disable_web_page_preview': True},
    {'disable_notification': True},
    {'disable_web_page_preview': True, 'disable_notification': True},
])
def test_send_message_with_params(get_token: str, get_chat_id: int, param: t.Dict):
    """Отправка сообщения с параметрами"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'{param=}\ntest send message with param.\n{test_name} https://github.com/'

    client = Telegram(token=get_token, chat_id=get_chat_id)
    result = client.send_message(msg, **param)

    assert result is True


@pytest.mark.parametrize('token,chat_id,param', [
    ('qweqweqwe', 123123123, {'disable_web_page_preview': True},),
    ('qweqweqwe', 123123123, {'disable_notification': True},),
    ('qweqweqwe', 123123123, {'disable_web_page_preview': True, 'disable_notification': True}),
])
def test_send_message_with_params_exception(token: str, chat_id: int, param: t.Dict):
    """Отлов ошибки при отправке сообщения в два чата при невалидных кредах"""
    client = Telegram(token=token, chat_id=chat_id)
    with pytest.raises(ConfigError):
        _ = client.send_message('', **param)


@pytest.mark.parametrize('param', [
    {'disable_web_page_preview': True},
    {'disable_notification': True},
    {'disable_web_page_preview': True, 'disable_notification': True},
])
def test_send_message_two_chat_ids_with_params(get_token: str, get_chat_id: int, param: t.Dict):
    """Отправка сообщения с параметрами в два чата"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'{param=}\ntest send message with param to many chat.\n{test_name} https://github.com/'

    client = Telegram(token=get_token, chat_id=[get_chat_id, get_chat_id])
    result = client.send_message(msg, **param)

    assert result is True


@pytest.mark.parametrize('token,chat_id,param', [
    ('qweqweqwe', 123123123, {'disable_web_page_preview': True},),
    ('qweqweqwe', 123123123, {'disable_notification': True},),
    ('qweqweqwe', 123123123, {'disable_web_page_preview': True, 'disable_notification': True}),
])
def test_send_message_two_chat_ids_with_params_exception(token: str, chat_id: int, param: t.Dict):
    """Отправка сообщения с параметрами в два чата"""
    client = Telegram(token=token, chat_id=chat_id)
    with pytest.raises(ConfigError):
        _ = client.send_message('msg', **param)


def test_send_message_env(get_token: str, get_chat_id: int):
    """Отправка сообщения с кредами из env-a"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f"test base send_message. with link preview https://github.com {test_name}"

    del os.environ['EASY_NOTIFYER_TELEGRAM_TOKEN']
    del os.environ['EASY_NOTIFYER_TELEGRAM_CHAT_ID']

    os.environ['EASY_NOTIFYER_TELEGRAM_TOKEN'] = get_token
    os.environ['EASY_NOTIFYER_TELEGRAM_CHAT_ID'] = str(get_chat_id)

    client = Telegram()
    result = client.send_message(msg)

    assert result is True


def test_send_message_env_clean_exception(get_token: str, get_chat_id: int):
    """Проверка ошибки на создание экземпляра без кредов"""
    del os.environ['EASY_NOTIFYER_TELEGRAM_TOKEN']
    del os.environ['EASY_NOTIFYER_TELEGRAM_CHAT_ID']
    with pytest.raises(ConfigError):
        _ = Telegram()


def test_send_message_two_chat_ids_env(get_token: str, get_chat_id: int):
    """Отправка сообщений в два чата с кредами из env-a"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'test two chat_ids(2 msg to one chat id) send message. {test_name}'

    os.environ['EASY_NOTIFYER_TELEGRAM_TOKEN'] = get_token
    os.environ['EASY_NOTIFYER_TELEGRAM_CHAT_ID'] = ','.join([str(get_chat_id) for _ in range(2)])

    client = Telegram()
    result = client.send_message(msg)

    assert result is True


def test_send_message_two_chat_ids_env_exception(get_token: str, get_chat_id: int):
    """Проверка отправки сообщения с невалидным токеном из энва"""
    test_name = inspect.currentframe().f_code.co_name
    msg = f'test two chat_ids(2 msg to one chat id) send message. {test_name}'

    os.environ['EASY_NOTIFYER_TELEGRAM_TOKEN'] = get_token
    os.environ['EASY_NOTIFYER_TELEGRAM_CHAT_ID'] = ''.join([str(get_chat_id) for _ in range(2)])

    client = Telegram()
    with pytest.raises(ConfigError):
        _ = client.send_message(msg)


# send attach
def test_send_attach_str(get_token: str, get_chat_id: int):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=get_token, chat_id=get_chat_id)

    result = client.send_attach(f"test send str attach. {test_name}")

    assert result is True


@pytest.mark.parametrize('token,chat_id', [
    ('qweqweqwe', 123123123),
    ('foobar', 00000000),
])
def test_send_attach_str_exception(token: str, chat_id: int):
    """Проверка отправки файла"""
    client = Telegram(token=token, chat_id=chat_id)
    with pytest.raises(ConfigError):
        _ = client.send_attach("test send str attach.")


@pytest.mark.parametrize('param', [
    {'disable_notification': True},
])
def test_send_attach_str_with_params(get_token: str, get_chat_id: int, param: t.Dict):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=get_token, chat_id=get_chat_id)

    result = client.send_attach(f"test send str attach. {test_name}", **param)

    assert result is True


@pytest.mark.parametrize('token,chat_id,param', [
    ('qweqweqwe', 123123123, {'disable_notification': True},),
])
def test_send_attach_str_with_params_exception(token: str, chat_id: int, param: t.Dict):
    """Отлов ошибки при отправке файла с выключенными уведомлениями"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=token, chat_id=chat_id)

    with pytest.raises(ConfigError):
        _ = client.send_attach(f"test send str attach. {test_name}", **param)


def test_send_attach_str_two_chat_ids(get_token: str, get_chat_id: int):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=get_token, chat_id=[get_chat_id, get_chat_id])

    result = client.send_attach(f"test send str attach. {test_name}")

    assert result is True


@pytest.mark.parametrize('token,chat_id', [
    ('qweqweqwe', [123123123, 00000000]),
    ('foobar', [123123123, 00000000]),
])
def test_send_attach_str_two_chat_ids_exception(token: str, chat_id: int):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=token, chat_id=chat_id)

    with pytest.raises(ConfigError):
        _ = client.send_attach(f"test send str attach. {test_name}")


@pytest.mark.parametrize('param', [
    {'disable_notification': True},
])
def test_send_attach_str_two_chat_ids_params(get_token: str, get_chat_id: int, param: t.Dict):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=get_token, chat_id=[get_chat_id, get_chat_id])

    result = client.send_attach(f"test send str attach. {test_name}", **param)

    assert result is True


@pytest.mark.parametrize('token,chat_id,param', [
    ('qweqweqwe', [123123123, 123123123], {'disable_notification': True},),
])
def test_send_attach_str_two_chat_ids_params_exception(
        token: str, chat_id: t.List[int], param: t.Dict
):
    """Проверка отправки файла"""
    test_name = inspect.currentframe().f_code.co_name
    client = Telegram(token=token, chat_id=chat_id)

    with pytest.raises(ConfigError):
        _ = client.send_attach(f"test send str attach. {test_name}", **param)


# def test_from_env_params_send_attach(get_token, get_chat_id):
#     test_name = inspect.currentframe().f_code.co_name
#     msg = f"test base send attach with creds from env. {test_name}"
#
#     client = Telegram()
#     client.send_attach()


# def test_from_env_params_send_attach_bytes(set_token, set_chat_id):
#     test_name = inspect.currentframe().f_code.co_name
#     file = b'some data'
#     client = Telegram()
#     client.send_attach(
#         file,
#         msg=f"test base send attach bytes with creds from env. {test_name}",
#     )
#
#
# def test_from_env_params_send_attach_bytes_filename(set_token, set_chat_id):
#     test_name = inspect.currentframe().f_code.co_name
#     file = b'some data with filename'
#     client = Telegram()
#     client.send_attach(
#         file,
#         msg=f"test base send attach bytes with creds from env. {test_name}",
#         filename='some data with filename.txt'
#     )
#
#
# def test_send_str_attach_with_msg(self):
#     test_name = inspect.currentframe().f_code.co_name
#     self._client.send_attach(
#         f"test send str attach with msg. {test_name}",
#         msg=f"test send str attach with msg. {test_name}",
#     )
#
#
# def test_send_str_attach_with_msg_filename(self):
#     test_name = inspect.currentframe().f_code.co_name
#     self._client.send_attach(
#         f"test send str attach with msg. {test_name}",
#         msg=f"test send str attach with msg, filename. {test_name}",
#         filename=f"some filename for str.txt",
#     )
#
#
# def test_send_str_attach_with_msg_filename_disable_notification(
#         self,
#         disable_notification_params,
# ):
#     test_name = inspect.currentframe().f_code.co_name
#     self._client.send_attach(
#         f"test send str attach with msg, filename, disable notification. {test_name}",
#         msg=f"test send str attach with msg, filename, disable notification. {test_name}",
#         filename=f"some filename for str.txt",
#         **disable_notification_params
#     )
#
#
# def test_send_attach_two_chat_ids(get_token: str, get_chat_id: int):
#     test_name = inspect.currentframe().f_code.co_name
#     two_tokens = [get_chat_id, get_chat_id]
#     file = f'test two chat_ids(2 msg to one chat id) send message. {test_name}'
#     msg = 'qwe'
#
#     client = Telegram(token=get_token, chat_id=two_tokens)
#     result = client.send_attach(file, msg=msg)
#
#     assert result is True
#
#
# def test_from_env_params_send_message():
#     test_name = inspect.currentframe().f_code.co_name
#     msg = f"test base send_message with creds from env. {test_name}"
#
#     client = Telegram()
#     result = client.send_message(msg)
#
#     assert result is True
