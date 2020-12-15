import os
import traceback
from functools import wraps
from typing import Optional, Union, List

from easy_notifyer.clients import AsyncRequests, Requests
from easy_notifyer.utils import make_report, get_telegram_creds


class TelegramBase:
    API_BASE_URL = os.getenv('EASY_NOTIFYER_API_BASE_URL', 'https://api.telegram.org/')
    API_BASE_URL = API_BASE_URL[:-1] if API_BASE_URL.endswith('/') else API_BASE_URL

    def __init__(self, token: str, chat_id: Union[int, List[int]]):
        self._token = token
        self._chat_id = chat_id
        self._request_url = f"{self.API_BASE_URL}/bot{self._token}/"


class TelegramAsync(TelegramBase):
    def __init__(self, token: str, chat_id: int):
        super().__init__(token, chat_id)
        self._client = AsyncRequests()

    def send_report(self):
        pass


class Telegram(TelegramBase):
    def __init__(self, token: str, chat_id: Union[int, List[int]]):
        """
        https://core.telegram.org/bots#6-botfather
        https://api.telegram.org/bot<TOKEN>/getUpdates
        :param token:
        :param chat_id:
        """
        super().__init__(token, chat_id)
        self._client = Requests()

    def _send_request(self, *, method_api: str, method_req: str, **kwargs):
        method = getattr(self._client, method_req)
        method(url=self._request_url + method_api, **kwargs)

    def send_message(self, msg: str, **kwargs):
        method_api = 'sendMessage'
        chat_ids = [self._chat_id] if isinstance(self._chat_id, int) else self._chat_id

        for chat_id in chat_ids:
            body = {
                'chat_id': chat_id,
                'text': msg,
            }
            if kwargs.get('parse_mode'):
                body['parse_mode'] = kwargs['parse_mode']
            if kwargs.get('disable_web_page_preview'):
                body['disable_web_page_preview'] = True
            self._send_request(method_api=method_api, method_req='post', json=body, **kwargs)

    def send_report(self, tback: str, func_name: Optional[str] = None):
        report = make_report(tback, func_name)
        self.send_message(report)


def telegram_reporter(*, token: Optional[str] = None, chat_id: Optional[int] = None, **params):
    exceptions = params.get('exceptions', Exception)
    if token is None or chat_id is None:
        token, chat_id = get_telegram_creds()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                bot = Telegram(token=token, chat_id=chat_id)
                bot.send_report(tback, func_name)
                raise exc
        return wrapper()
    return decorator
