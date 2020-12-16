from typing import Any, Dict, Union, IO

from httpx import AsyncClient, Client, Response


class AsyncRequests:
    def __init__(self):
        self._client = AsyncClient()

    async def post(
            self,
            *,
            url: str,
            params: Dict,
            body: Dict,
            data: Any,
            files: Union[IO[str], IO[bytes], str, bytes],
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
            params: Dict,
            body: Dict,
            data: Any,
            files: Union[IO[str], IO[bytes], str, bytes],
    ) -> Response:
        return self._client.post(url=url, params=params, json=body, data=data, files=files)
