import pytest

from easy_notifyer.clients.requests import AsyncRequests, Requests


@pytest.fixture(scope="function")
def client():
    return Requests()


@pytest.fixture(scope="function")
def async_client():
    return AsyncRequests()
