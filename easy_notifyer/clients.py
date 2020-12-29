# pylint: disable=too-few-public-methods
from http.client import HTTPResponse as Response
from typing import Dict, Optional
from urllib import request
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from easy_notifyer.types import MultiPartForm
from easy_notifyer.utils import run_sync


class RequestsBase:
    """Base requests obj"""
    @staticmethod
    def _add_params(url: str, params: Dict) -> str:
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)


class Requests(RequestsBase):
    """Client for requests"""
    def __init__(self):
        self._client = request.Request

    def post(
            self,
            *,
            url: str,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None,
            files: Optional[Dict] = None,
    ) -> Response:
        """Send post request"""
        data = None
        if params is not None:
            url = self._add_params(url, params)
        if body is not None or files is not None:
            form = MultiPartForm(body=body, files=files)
            data = bytes(form)
            headers = {**headers, **form.header} if headers is not None else form.header

        req = self._client(url=url, headers=headers, data=data)
        resp = request.urlopen(req)
        setattr(resp, 'status_code', resp.status)
        return resp


class AsyncRequests:
    """Async client for requests"""
    def __init__(self):
        self._client = Requests()

    async def post(
            self,
            *,
            url: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            body: Optional[Dict] = None,
            files: Optional[Dict] = None,
    ) -> Response:
        """Send async post request"""
        return await run_sync(
            self._client.post,
            url=url,
            headers=headers,
            params=params,
            body=body,
            files=files
        )
