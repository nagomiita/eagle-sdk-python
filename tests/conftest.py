import pytest

from eagle_sdk import EagleClient


@pytest.fixture
def client() -> EagleClient:
    return EagleClient(base_url="http://localhost:41595")
