import functools
import traceback
import uuid
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

from easy_notifyer.clients import AsyncRequests, Requests, Response
from easy_notifyer.env import Env
from easy_notifyer.report import Report
from easy_notifyer.utils import get_telegram_creds, run_sync


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
            data: Optional[Dict] = None,
            files: Optional[Dict] = None
    ) -> Response:
        return await self._client.post(
            url=self._request_url + method_api,
            params=params,
            body=body,
            data=data,
            files=files,
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

    async def send_attach(
            self,
            msg: str,
            attach: Union[bytes, str, Tuple],
            filename: Optional[str] = None
    ):
        method_api = 'sendDocument'
        chat_ids = [self._chat_id] if isinstance(self._chat_id, int) else self._chat_id
        filename = filename or uuid.uuid4().hex

        files = {}
        if isinstance(attach, tuple):
            files['document'] = attach
        elif isinstance(attach, bytes):
            files['document'] = (filename, BytesIO(attach))
        else:
            files['document'] = (filename, BytesIO(attach.encode()))

        params = {}
        if msg is not None:
            params['caption'] = msg

        for chat_id in chat_ids:
            params['chat_id'] = chat_id
            await self._send_post(method_api=method_api, params=params, files=files)

    async def send_report(self, report: Report, **kwargs):
        if report.attach is not None:
            date = datetime.now().replace(microsecond=0).strftime(
                Env.EASY_NOTIFYER_FILENAME_DT_FORMAT
            )
            filename = f"{date}.txt"
            await self.send_attach(msg=report.report, attach=report.attach, filename=filename)
        else:
            await self.send_message(report.report, **kwargs)


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
            data: Optional[Dict] = None,
            files: Optional[Dict] = None,
    ) -> Response:
        return self._client.post(
            url=self._request_url + method_api,
            params=params,
            body=body,
            data=data,
            files=files
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

    def send_attach(
            self,
            msg: str,
            attach: Union[bytes, str, Tuple],
            filename: Optional[str] = None
    ):
        method_api = 'sendDocument'
        chat_ids = [self._chat_id] if isinstance(self._chat_id, int) else self._chat_id
        filename = filename or uuid.uuid4().hex

        files = {}
        if isinstance(attach, tuple):
            files['document'] = attach
        elif isinstance(attach, bytes):
            files['document'] = (filename, BytesIO(attach))
        else:
            files['document'] = (filename, BytesIO(attach.encode()))

        params = {}
        if msg is not None:
            params['caption'] = msg

        for chat_id in chat_ids:
            params['chat_id'] = chat_id
            self._send_post(method_api=method_api, params=params, files=files)

    def send_report(self, report: Report, **kwargs):
        if report.attach is not None:
            date = datetime.now().replace(microsecond=0).strftime(
                Env.EASY_NOTIFYER_FILENAME_DT_FORMAT
            )
            filename = f"{date}.txt"
            self.send_attach(msg=report.report, attach=report.attach, filename=filename)
        else:
            self.send_message(report.report, **kwargs)


def _report_maker(
        *,
        tback: str,
        func_name: Optional[str] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
) -> Report:
    return Report(tback, func_name, header, as_attached)


def telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
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
                report = _report_maker(
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                bot.send_report(report, **params)
                raise exc
        return wrapper
    return decorator


def async_telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
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
                report = await run_sync(
                    _report_maker,
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                bot = TelegramAsync(token=token, chat_id=chat_id)
                await bot.send_report(report, **params)
                raise exc
        return wrapper
    return decorator
