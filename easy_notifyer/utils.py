import asyncio
import functools
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

from easy_notifyer.env import Env
from easy_notifyer.exceptions import ConfigError


class MultiPartForm:
    """Creating body of request"""
    def __init__(self, body: Optional[Dict] = None, files: Optional[Dict] = None):
        self._body = body
        self._files = files
        self.boundary = uuid4().hex

    def __bytes__(self):
        return self.encode()

    @staticmethod
    def _form_data(name: str) -> str:
        """Get formdata for input in body"""
        return f'Content-Disposition: form-data; name="{name}"'

    @staticmethod
    def _attached_file(name: str, filename: str) -> str:
        """Get formdata of file for input in body"""
        return f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'

    @property
    def header(self) -> Dict[str, str]:
        """Get a header request"""
        return {'Content-type': f'multipart/form-data; boundary={self.boundary}'}

    def encode(self) -> bytes:
        """Create a body request."""
        body = []
        boundary = b'--' + self.boundary.encode('utf-8')
        if self._body is not None and isinstance(self._body, dict):
            for name, value in self._body.items():
                body.append(boundary)
                body.append(self._form_data(name).encode('utf-8'))
                body.append(b'')
                body.append(str(value).encode('utf-8'))

        if self._files is not None and isinstance(self._files, dict):
            for fieldname in self._files:
                if len(self._files[fieldname]) != 2:
                    continue
                filename, data = self._files[fieldname]
                body.append(boundary)
                body.append(self._attached_file(fieldname, filename).encode('utf-8'))
                body.append(b'')
                if hasattr(data, 'read') is True:
                    data.seek(0)
                    body.append(data.read())
                elif hasattr(data, 'encode') is True:
                    body.append(data.encode('utf-8'))

        body.append(boundary + b'--')
        return b"\r\n".join(body)


def get_telegram_creds() -> Tuple[str, List[int]]:
    """
    Get telegram creds from environment variable
    Returns:
        Tuple[token(str), List[chat_id(int), ...]]
    """
    token = Env().EASY_NOTIFYER_TELEGRAM_TOKEN
    chat_id = Env().EASY_NOTIFYER_TELEGRAM_CHAT_ID

    error = ConfigError(token=token, chat_id=chat_id)

    if token is None or chat_id is None:
        raise error
    try:
        chat_id = [i.strip() for i in chat_id.split(',')]
        chat_id = [int(i) for i in chat_id if i]
    except ValueError as exc:
        raise error from exc
    return token, chat_id


async def run_async(func: Callable, *args, **kwargs) -> Any:
    """
    Run sync func in async code in thread pool.
    Args:
        func(callable): func to run
        *args:
        **kwargs:
    Returns:
        same as func
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
