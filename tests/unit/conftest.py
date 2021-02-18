import pytest

from easy_notifyer.clients import Requests, AsyncRequests


@pytest.fixture(scope='function')
def client():
    return Requests()


@pytest.fixture(scope='function')
def async_client():
    return AsyncRequests()
