import inspect
import typing as t

import pytest

from easy_notifyer import Telegram


class BaseTelegram:
    @pytest.fixture(autouse=True)
    def get_client(self, ready_client: Telegram):
        self._client = ready_client


class TestTelegramSendMessage(BaseTelegram):
    @staticmethod
    def test_from_env_params_send_message(set_token, set_chat_id):
        test_name = inspect.currentframe().f_code.co_name
        client = Telegram()
        client.send_message(f"test base send_message with creds from env. {test_name}")

    def test_base_send_message(self):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_message(f"test base send_message. "
                                  f"with link preview https://github.com {test_name}")

    @staticmethod
    def test_send_message_two_chat_ids(get_token: str, get_chat_id: t.List[int]):
        test_name = inspect.currentframe().f_code.co_name
        two_tokens = get_chat_id + get_chat_id
        client = Telegram(token=get_token, chat_id=two_tokens)
        client.send_message(f'test two chat_ids(2 msg to one chat id) send message. {test_name}')

    def test_send_message_without_notification(self, disable_notification_params: t.Dict):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_message(
            f'test send message without notification {test_name}',
            **disable_notification_params
        )

    def test_send_message_without_web_page_preview(self, disable_web_page_preview_params: t.Dict):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_message(
            f'test send message without web page preview https://github.com {test_name}',
            **disable_web_page_preview_params
        )

    def test_send_message_two_params(
            self,
            disable_web_page_preview_params,
            disable_notification_params,
    ):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_message(
            f'test send message without web page preview and without notification '
            f'https://github.com {test_name}',
            **{**disable_notification_params, **disable_web_page_preview_params}
        )


class TestTelegramSendAttach(BaseTelegram):
    @staticmethod
    def test_from_env_params_send_attach(set_token, set_chat_id):
        test_name = inspect.currentframe().f_code.co_name
        client = Telegram()
        client.send_attach(
            f"test base send attach with creds from env. {test_name}",
        )

    @staticmethod
    def test_from_env_params_send_attach_bytes(set_token, set_chat_id):
        test_name = inspect.currentframe().f_code.co_name
        file = b'some data'
        client = Telegram()
        client.send_attach(
            file,
            msg=f"test base send attach bytes with creds from env. {test_name}",
        )

    @staticmethod
    def test_from_env_params_send_attach_bytes_filename(set_token, set_chat_id):
        test_name = inspect.currentframe().f_code.co_name
        file = b'some data with filename'
        client = Telegram()
        client.send_attach(
            file,
            msg=f"test base send attach bytes with creds from env. {test_name}",
            filename='some data with filename.txt'
        )

    def test_send_str_attach(self):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_attach(f"test send str attach. {test_name}")

    def test_send_str_attach_with_msg(self):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_attach(
            f"test send str attach with msg. {test_name}",
            msg=f"test send str attach with msg. {test_name}",
        )

    def test_send_str_attach_with_msg_filename(self):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_attach(
            f"test send str attach with msg. {test_name}",
            msg=f"test send str attach with msg, filename. {test_name}",
            filename=f"some filename for str.txt",
        )

    def test_send_str_attach_with_msg_filename_disable_notification(
            self,
            disable_notification_params,
    ):
        test_name = inspect.currentframe().f_code.co_name
        self._client.send_attach(
            f"test send str attach with msg, filename, disable notification. {test_name}",
            msg=f"test send str attach with msg, filename, disable notification. {test_name}",
            filename=f"some filename for str.txt",
            **disable_notification_params
        )

    # @staticmethod
    # def test_send_attach_two_chat_ids(get_token: str, get_chat_id: t.List[int]):
    #     test_name = inspect.currentframe().f_code.co_name
    #     two_tokens = get_chat_id + get_chat_id
    #     client = Telegram(token=get_token, chat_id=two_tokens)
    #     client.send_attach(
    #         f'test two chat_ids(2 msg to one chat id) send message. {test_name}',
    #         msg='qwe',
    #     )
