from typing import Dict

import pytest
from pytest_mock import MockerFixture

from easy_notifyer import clients
from easy_notifyer.clients import Requests as Requests


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.unit,
]


@pytest.mark.parametrize(
    "url, params, result",
    [
        (
            "http://example.com",
            {"foo": "bar", "hello": "world"},
            "http://example.com?foo=bar&hello=world",
        ),
    ],
)
def test_add_params(
    client: Requests,
    mocker: MockerFixture,
    url: str,
    params: Dict,
    result: str,
):
    mocker.patch.object(client, "_client")
    mocker.patch.object(clients, "request")
    mocker.patch.object(clients, "HTTPResponse")
    client.post(
        url=url,
        params=params,
    )
    client._client.assert_called_once_with(
        url=result,
        headers={},
        data=None,
    )


class TestRequests:
    pass


class TestAsyncRequests:
    pass


class TestResponse:
    pass
