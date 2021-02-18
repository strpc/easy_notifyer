# pylint: disable=too-few-public-methods
import logging
import uuid
from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO, Dict, List, Optional, Tuple, Union
from urllib.error import HTTPError

from easy_notifyer.clients import AsyncRequests, Requests
from easy_notifyer.env import Env
from easy_notifyer.exceptions import ConfigError
from easy_notifyer.utils import get_telegram_creds, run_async


logger = logging.getLogger(__name__)


class ITelegram(ABC):
    @abstractmethod
    def send_message(self, msg: str, **kwargs) -> Optional[bool]:
        ...

    @abstractmethod
    def send_attach(
        self,
        attach: Union[bytes, str, BinaryIO, Tuple[str, Union[BinaryIO, bytes]]],
        *,
        msg: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs,
    ) -> Optional[bool]:
        ...


class TelegramBase:
    """Base class of telegram"""

    API_BASE_URL = Env().EASY_NOTIFYER_TELEGRAM_API_URL
    API_BASE_URL = API_BASE_URL[:-1] if API_BASE_URL.endswith("/") else API_BASE_URL

    def __init__(
        self,
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        if token is None or chat_id is None:
            token, chat_id = get_telegram_creds()
        self._token = token
        self._chat_ids = [chat_id] if isinstance(chat_id, int) else chat_id
        self._base_api_url = f"{self.API_BASE_URL}/bot{self._token}/"

    @staticmethod
    def _prepare_attach(
        *,
        attach: Union[bytes, str, BinaryIO, Tuple[str, Union[BinaryIO, bytes]]],
        filename: Optional[str] = None,
    ) -> Dict:
        """
        Preparation of attach for sending to telegram
        Args:
            attach(bytes, str, binaryio, tuple): attach to send
            filename: filename
        Returns:
            {'document': (filename, b'file)}
        """
        filename = filename or uuid.uuid4().hex
        files = {}
        if isinstance(attach, tuple) is True:
            files["document"] = attach
        elif isinstance(attach, bytes) is True:
            files["document"] = (filename, BytesIO(attach))
        elif hasattr(attach, "read") and isinstance(attach.read(0), bytes):
            files["document"] = (filename, attach)
        else:
            files["document"] = (filename, BytesIO(attach.encode()))
        return files


class TelegramAsync(ITelegram, TelegramBase):
    """Async client for telegram"""

    def __init__(
        self,
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        super().__init__(token=token, chat_id=chat_id)
        self._client = AsyncRequests()

    async def _send_post(
        self,
        *,
        method_api: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ):
        """
        Send async post request.
        Args:
            method_api(str): method of api telegram
            headers(dict, optional): headers for of request.
            params(dict, optional): params of request.
            body(dict, optional): body of request.
            files(dict, optional): files of request in format ('filename.txt', b'filedata').

        Returns:
            instance of Response.
        """
        try:
            response = await self._client.post(
                url=self._base_api_url + method_api,
                headers=headers,
                params=params,
                body=body,
                files=files,
            )
        except HTTPError as error:
            raise ConfigError(token=self._token, chat_id=self._chat_ids, error=error) from error
        except Exception:
            logger.error("Send message to telegram error. Response: %s", response.read())
        return response

    async def send_message(self, msg: str, **kwargs) -> Optional[bool]:
        """
        Send message.
        Args:
            msg(str): text of message.
            **kwargs:
                disable_notification(bool): True to disable notification of message.
                disable_web_page_preview(bool): True to disable web preview for links.
        """
        method_api = "sendMessage"

        for chat_id in self._chat_ids:
            body = {
                "chat_id": chat_id,
                "text": msg,
            }
            if kwargs.get("disable_web_page_preview") is not None:
                body["disable_web_page_preview"] = True
            if kwargs.get("disable_notification") is not None:
                body["disable_notification"] = True
            await self._send_post(method_api=method_api, body=body)
        return True

    async def send_attach(
        self,
        attach: Union[bytes, str, BinaryIO, Tuple[str, Union[BinaryIO, bytes]]],
        *,
        msg: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs,
    ) -> Optional[bool]:
        """
        Send file.
        Args:
            attach (bytes, str, tuple): file to send. if tuple, then
            ('filename.txt', b'text of file').
            msg (str, optional): text of message.
            filename(str, optional): filename if attach is string or bytes.
            **kwargs:
                disable_notification(bool): True to disable notification of message.
        """
        method_api = "sendDocument"
        files = await run_async(self._prepare_attach, attach=attach, filename=filename)

        params = {}
        if msg is not None:
            params["caption"] = msg
        if kwargs.get("disable_notification") is not None:
            params["disable_notification"] = True

        for chat_id in self._chat_ids:
            params["chat_id"] = chat_id
            await self._send_post(method_api=method_api, params=params, files=files)
        return True


class Telegram(ITelegram, TelegramBase):
    """Client of telegram"""

    def __init__(
        self,
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
    ):
        """
        Args:
            token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
            chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        """
        super().__init__(token=token, chat_id=chat_id)
        self._client = Requests()

    def _send_post(
        self,
        *,
        method_api: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ):
        """
        Send post request.
        Args:
            method_api(str): method of api telegram
            headers(dict, optional): headers for of request.
            params(dict, optional): params of request.
            body(dict, optional): body of request.
            files(dict, optional): files of request in format ('filename.txt', b'filedata').

        Returns:
            instance of Response.
        """
        try:
            response = self._client.post(
                url=self._base_api_url + method_api,
                headers=headers,
                params=params,
                body=body,
                files=files,
            )
        except HTTPError as error:
            raise ConfigError(token=self._token, chat_id=self._chat_ids, error=error) from error
        except Exception:
            logger.error("Send message to telegram error. Response: %s", response.read())
        return response

    def send_message(self, msg: str, **kwargs) -> True:
        """
        Send message.
        Args:
            msg(str): text of message.
            **kwargs:
                disable_notification(bool): True to disable notification of message.
                disable_web_page_preview(bool): True to disable web preview for links.
        """
        method_api = "sendMessage"

        for chat_id in self._chat_ids:
            body = {
                "chat_id": chat_id,
                "text": msg,
            }
            if kwargs.get("disable_web_page_preview") is not None:
                body["disable_web_page_preview"] = True
            if kwargs.get("disable_notification") is not None:
                body["disable_notification"] = True
            self._send_post(method_api=method_api, body=body)
        return True

    def send_attach(
        self,
        attach: Union[bytes, str, BinaryIO, Tuple[str, Union[BinaryIO, bytes]]],
        *,
        msg: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs,
    ) -> Optional[bool]:
        """
        Send file.
        Args:
            attach (bytes, str, tuple): file to send. if tuple, then
            ('filename.txt', b'text of file').
            msg (str, optional): text of message.
            filename(str, optional): filename if attach is string or bytes.
            **kwargs:
                disable_notification(bool): True to disable notification of message.
        """
        method_api = "sendDocument"
        files = self._prepare_attach(attach=attach, filename=filename)

        params = {}
        if msg is not None:
            params["caption"] = msg
        if kwargs.get("disable_notification") is not None:
            params["disable_notification"] = True

        for chat_id in self._chat_ids:
            params["chat_id"] = chat_id
            self._send_post(method_api=method_api, params=params, files=files)
        return True
