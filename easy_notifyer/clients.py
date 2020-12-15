from httpx import AsyncClient, Client


class AsyncRequests:
    def __init__(self):
        self._client = AsyncClient()

    async def post(self, *args, **kwargs):
        self._client.post(*args, **kwargs)


class Requests:
    def __init__(self):
        self._client = Client()

    def post(self, *args, **kwargs):
        return self._client.post(*args, **kwargs)
