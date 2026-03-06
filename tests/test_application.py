import pytest
from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient


class TestApplicationAPI:
    def test_info(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/application/info",
            json={
                "status": "success",
                "data": {
                    "version": "1.11.0",
                    "prereleaseVersion": None,
                    "buildVersion": "20200612",
                    "execPath": "/path/to/eagle",
                    "platform": "darwin",
                },
            },
        )

        info = client.application.info()

        assert info.version == "1.11.0"
        assert info.prerelease_version is None
        assert info.build_version == "20200612"
        assert info.exec_path == "/path/to/eagle"
        assert info.platform == "darwin"
