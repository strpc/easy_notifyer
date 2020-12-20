import functools
import traceback
import uuid
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Type, Union

from easy_notifyer.clients import AsyncRequests, Requests, Response
from easy_notifyer.env import Env
from easy_notifyer.report import Report
from easy_notifyer.utils import get_telegram_creds, run_sync


class TelegramBase:
    API_BASE_URL = Env.EASY_NOTIFYER_TELEGRAM_API_URL
    API_BASE_URL = API_BASE_URL[:-1] if API_BASE_URL.endswith('/') else API_BASE_URL

    def __init__(
            self,
            *,
            token: Optional[str] = None,
            chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        if token is None or chat_id is None:
            token, chat_id = get_telegram_creds()
        self._token = token
        self._chat_ids = [chat_id] if isinstance(chat_id, int) else chat_id
        self._base_api_url = f"{self.API_BASE_URL}/bot{self._token}/"


class TelegramAsync(TelegramBase):
    def __init__(
            self,
            *,
            token: Optional[str] = None,
            chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        super().__init__(token=token, chat_id=chat_id)
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
        """
        Send async post request.
        Args:
            method_api(str): method of api telegram
            params(dict, optional): params of request.
            body(dict, optional): body of request.
            data(dict, optional): data of request.
            files(dict, optional): files of request in format ('filename.txt', b'filedata').

        Returns:
            instance of Response.
        """
        return await self._client.post(
            url=self._base_api_url + method_api,
            params=params,
            body=body,
            data=data,
            files=files,
        )

    async def send_message(self, msg: str, **kwargs):
        """
        Send message.
        Args:
            msg(str): text of message.
            **kwargs:
                parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
                disable_notification(bool): True to disable notification of message.
                disable_web_page_preview(bool): True to disable web preview for links.
        """
        method_api = 'sendMessage'

        for chat_id in self._chat_ids:
            body = {
                'chat_id': chat_id,
                'text': msg,
            }
            if kwargs.get('parse_mode') is not None:
                body['parse_mode'] = kwargs['parse_mode']
            if kwargs.get('disable_web_page_preview') is not None:
                body['disable_web_page_preview'] = True
            if kwargs.get('disable_notification') is not None:
                body['disable_notification'] = True
            await self._send_post(method_api=method_api, body=body)

    async def send_attach(
            self,
            attach: Union[bytes, str, Tuple],
            msg: Optional[str] = None,
            filename: Optional[str] = None,
            **kwargs
    ):
        """
        Send file.
        Args:
            attach (bytes, str, tuple): file to send. if tuple, then
            ('filename.txt', b'text of file').
            msg (str, optional): text of message.
            filename(str, optional): filename if attach is string or bytes.
            **kwargs:
                parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
                disable_notification(bool): True to disable notification of message.
        """
        method_api = 'sendDocument'
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
        if kwargs.get('parse_mode') is not None:
            params['parse_mode'] = kwargs['parse_mode']
        if kwargs.get('disable_notification') is not None:
            params['disable_notification'] = True

        for chat_id in self._chat_ids:
            params['chat_id'] = chat_id
            await self._send_post(method_api=method_api, params=params, files=files)


class Telegram(TelegramBase):
    def __init__(
            self,
            *,
            token: Optional[str] = None,
            chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        super().__init__(token=token, chat_id=chat_id)
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
        """
        Send post request.
        Args:
            method_api(str): method of api telegram
            params(dict, optional): params of request.
            body(dict, optional): body of request.
            data(dict, optional): data of request.
            files(dict, optional): files of request in format ('filename.txt', b'filedata').

        Returns:
            instance of Response.
        """
        return self._client.post(
            url=self._base_api_url + method_api,
            params=params,
            body=body,
            data=data,
            files=files
        )

    def send_message(self, msg: str, **kwargs):
        """
        Send message.
        Args:
            msg(str): text of message.
            **kwargs:
                parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
                disable_notification(bool): True to disable notification of message.
                disable_web_page_preview(bool): True to disable web preview for links.
        """
        method_api = 'sendMessage'

        for chat_id in self._chat_ids:
            body = {
                'chat_id': chat_id,
                'text': msg,
            }
            if kwargs.get('parse_mode') is not None:
                body['parse_mode'] = kwargs['parse_mode']
            if kwargs.get('disable_web_page_preview') is not None:
                body['disable_web_page_preview'] = True
            if kwargs.get('disable_notification') is not None:
                body['disable_notification'] = True
            self._send_post(method_api=method_api, body=body)

    def send_attach(
            self,
            attach: Union[bytes, str, Tuple],
            msg: Optional[str] = None,
            filename: Optional[str] = None,
            **kwargs
    ):
        """
        Send file.
        Args:
            attach (bytes, str, tuple): file to send. if tuple, then
            ('filename.txt', b'text of file').
            msg (str, optional): text of message.
            filename(str, optional): filename if attach is string or bytes.
            **kwargs:
                parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
                disable_notification(bool): True to disable notification of message.
        """
        method_api = 'sendDocument'
        filename = filename or uuid.uuid4().hex

        files = {}
        if isinstance(attach, tuple) is True:
            files['document'] = attach
        elif isinstance(attach, bytes) is True:
            files['document'] = (filename, BytesIO(attach))
        else:
            files['document'] = (filename, BytesIO(attach.encode()))

        params = {}
        if msg is not None:
            params['caption'] = msg
        if kwargs.get('parse_mode') is not None:
            params['parse_mode'] = kwargs['parse_mode']
        if kwargs.get('disable_notification') is not None:
            params['disable_notification'] = True

        for chat_id in self._chat_ids:
            params['chat_id'] = chat_id
            self._send_post(method_api=method_api, params=params, files=files)


def _report_maker(
        *,
        tback: str,
        func_name: Optional[str] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
) -> Report:
    """
    Make report from
    Args:
        tback(str): traceback for report.
        func_name(str, optional): name of function when raised error.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for send as a file. Default - False.

    Returns:
        isinstance of Report obj.
    """
    return Report(tback, func_name, header, as_attached)


def _get_filename(filename: Optional[str] = None) -> str:
    """
    Generate of filename for send report as a file.
    Args:
        filename(str, optional): filename, if exists. Else - "{datetime}.txt". Format of datetime
        may be set in environment variable `EASY_NOTIFYER_FILENAME_DT_FORMAT`.
        Default - "%Y-%m-%d %H_%M_%S"
    Returns:
        string of filename.
    """
    if filename is None:
        date = datetime.now().replace(microsecond=0).strftime(
            Env.EASY_NOTIFYER_FILENAME_DT_FORMAT
        )
        filename = f"{date}.txt"
    return filename


def _report_handler(
        *,
        report: Report,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
        **kwargs
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): filename for send report as file.
            parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = Telegram(token=token, chat_id=chat_id)
    if report.attach is not None:
        filename = _get_filename(kwargs.pop('filename', None))
        bot.send_attach(msg=report.report, attach=report.attach, filename=filename, **kwargs)
    else:
        bot.send_message(report.report, **kwargs)


async def _async_report_handler(
        *,
        report: Report,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
        **kwargs
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): filename for send report as file.
            parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = TelegramAsync(token=token, chat_id=chat_id)
    if report.attach is not None:
        filename = await run_sync(_get_filename, kwargs.pop('filename', None))
        await bot.send_attach(msg=report.report, attach=report.attach, filename=filename, **kwargs)
    else:
        await bot.send_message(report.report, **kwargs)


def telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
    """
    Handler errors to send report in telegram.
    Args:
        token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        exceptions(exception, tuple(exception), optional): Exceptions for handle. Two and more - in
        tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for send as a file. Default - False.
        **params:
            filename(str, optional): filename for send report as file.
            parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    exceptions = exceptions or Exception

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                report = _report_maker(
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                _report_handler(report=report, token=token, chat_id=chat_id, **params)
                raise exc
        return wrapper
    return decorator


def async_telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
    """
    Async handler errors to send report in telegram.
    Args:
        token(str, optional): Telegram bot token. Can be used from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be used from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        exceptions(exception, tuple(exception), optional): Exceptions for handle. Two and more - in
        tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for send as a file. Default - False.
        **params:
            filename(str, optional): filename for send report as file.
            parse_mode(str): 'MarkdownV2', 'HTML' or 'Markdown' - style of formatting message.
                https://core.telegram.org/bots/api#formatting-options
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    exceptions = exceptions or Exception

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
                await _async_report_handler(report=report, token=token, chat_id=chat_id, **params)
                raise exc
        return wrapper
    return decorator
