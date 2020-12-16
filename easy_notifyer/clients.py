from typing import Any, Dict

from httpx import AsyncClient, Client, Response


class AsyncRequests:
    def __init__(self):
        self._client = AsyncClient()

    async def post(self, *, url: str, params: Dict, body: Dict, data: Any) -> Response:
        async with self._client as client:
            return await client.post(url=url, params=params, json=body, data=data)


class Requests:
    def __init__(self):
        self._client = Client()

    def post(self, *, url: str, params: Dict, body: Dict, data: Any) -> Response:
        return self._client.post(url=url, params=params, json=body, data=data)
