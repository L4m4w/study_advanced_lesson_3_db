import pytest

from tests.utils.base_session import BaseSession
from tests.utils.config import Server

@pytest.fixture(scope="session")
def local_api(env):
    address = Server(env).local_api
    with BaseSession(base_url=address) as session:
        yield session