"""transport 設定 (retries / limits) の配線テスト (#6)。"""

import httpx
from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient


def _transport(client: EagleClient) -> httpx.HTTPTransport:
    transport = client._http._client._transport
    assert isinstance(transport, httpx.HTTPTransport)
    return transport


class TestTransportWiring:
    def test_default_has_no_retries(self):
        transport = _transport(EagleClient())

        assert transport._pool._retries == 0

    def test_retries_is_wired_to_transport(self):
        transport = _transport(EagleClient(retries=2))

        assert transport._pool._retries == 2

    def test_limits_is_wired_to_transport(self):
        limits = httpx.Limits(max_connections=5, max_keepalive_connections=3)
        transport = _transport(EagleClient(limits=limits))

        assert transport._pool._max_connections == 5
        assert transport._pool._max_keepalive_connections == 3

    def test_requests_still_work_with_explicit_transport(self, httpx_mock: HTTPXMock):
        # pytest-httpx は明示 transport でもモックできる = 既存テスト互換の確認
        httpx_mock.add_response(
            json={"status": "success", "data": {"version": "4.0", "platform": "win32"}}
        )

        client = EagleClient(retries=1)
        info = client.application.info()

        assert info.version == "4.0"
