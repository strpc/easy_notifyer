import asyncio
import functools
import traceback
from typing import Union, List, Callable, Any, Dict, Optional

from easy_notifyer.clients import AsyncRequests, Requests, Response
from easy_notifyer.env import Env
from easy_notifyer.utils import make_report, get_telegram_creds


class TelegramBase:
    API_BASE_URL = Env.EASY_NOTIFYER_API_BASE_URL
    API_BASE_URL = API_BASE_URL[:-1] if API_BASE_URL.endswith('/') else API_BASE_URL

    def __init__(self, token: str, chat_id: Union[int, List[int]]):
        self._token = token
        self._chat_id = chat_id
        self._request_url = f"{self.API_BASE_URL}/bot{self._token}/"


class TelegramAsync(TelegramBase):
    def __init__(self, token: str, chat_id: int):
        super().__init__(token, chat_id)
        self._client = AsyncRequests()

    async def _send_post(
            self,
            *,
            method_api: str,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None,
            data: Optional[Any] = None
    ) -> Response:
        return await self._client.post(
            url=self._request_url + method_api,
            params=params,
            body=body,
            data=data,
        )

    async def send_message(self, msg: str, **kwargs):
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
            await self._send_post(method_api=method_api, body=body)

    async def send_report(self, tback: str, func_name: Optional[str] = None):
        report = await self._run_sync(make_report, tback, func_name)
        await self.send_message(report)

    @staticmethod
    async def _run_sync(func: Callable, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))


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

    def _send_post(
            self,
            *,
            method_api: str,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None,
            data: Optional[Any] = None,
    ) -> Response:
        return self._client.post(
            url=self._request_url + method_api,
            params=params,
            body=body,
            data=data,
        )

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
            self._send_post(method_api=method_api, body=body)

    def send_report(self, tback: str, func_name: Optional[str] = None):
        report = make_report(tback, func_name)
        self.send_message(report)


def telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[int] = None,
        **params
):
    exceptions = params.get('exceptions', Exception)
    if token is None or chat_id is None:
        token, chat_id = get_telegram_creds()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                bot = Telegram(token=token, chat_id=chat_id)
                bot.send_report(tback, func_name)
                raise exc
        return wrapper
    return decorator


def async_telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[int] = None,
        **params
):
    exceptions = params.get('exceptions', Exception)
    if token is None or chat_id is None:
        token, chat_id = get_telegram_creds()

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                bot = TelegramAsync(token=token, chat_id=chat_id)
                await bot.send_report(tback, func_name)
                raise exc
        return wrapper
    return decorator
