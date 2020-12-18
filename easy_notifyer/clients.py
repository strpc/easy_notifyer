from typing import Dict, Optional

from httpx import AsyncClient, Client, Response


class AsyncRequests:
    def __init__(self):
        self._client = AsyncClient()

    async def post(
            self,
            *,
            url: str,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None,
            data: Optional[Dict] = None,
            files: Optional[Dict] = None,
    ) -> Response:
        async with self._client as client:
            return await client.post(url=url, params=params, json=body, data=data, files=files)


class Requests:
    def __init__(self):
        self._client = Client()

    def post(
            self,
            *,
            url: str,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None,
            data: Optional[Dict] = None,
            files: Optional[Dict] = None,
    ) -> Response:
        return self._client.post(url=url, params=params, json=body, data=data, files=files)
