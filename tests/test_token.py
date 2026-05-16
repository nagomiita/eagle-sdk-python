import logging

from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient


class TestTokenSentOnRequests:
    def test_token_attached_to_get_request(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "status": "success",
                "data": {
                    "version": "4.0.0",
                    "prereleaseVersion": None,
                    "buildVersion": "build12",
                    "platform": "win32",
                },
            },
        )

        client = EagleClient(token="test-token-123")
        client.application.info()

        request = httpx_mock.get_request()
        assert request.url.params["token"] == "test-token-123"

    def test_token_attached_to_post_request(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"status": "success"})

        client = EagleClient(token="test-token-123")
        client.item.add_from_url(url="https://example.com/img.png", name="Test")

        request = httpx_mock.get_request()
        assert request.url.params["token"] == "test-token-123"

    def test_no_token_param_when_not_set(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "status": "success",
                "data": {
                    "version": "4.0.0",
                    "prereleaseVersion": None,
                    "buildVersion": "build12",
                    "platform": "win32",
                },
            },
        )

        client = EagleClient()
        client.application.info()

        request = httpx_mock.get_request()
        assert "token" not in request.url.params


class TestTokenMaskedInLogs:
    def test_sdk_logger_masks_token(self, httpx_mock: HTTPXMock, caplog):
        httpx_mock.add_response(
            json={
                "status": "success",
                "data": {
                    "version": "4.0.0",
                    "prereleaseVersion": None,
                    "buildVersion": "build12",
                    "platform": "win32",
                },
            },
        )

        client = EagleClient(token="secret-token-value")

        with caplog.at_level(logging.INFO, logger="eagle_sdk.http"):
            client.application.info()

        assert "token=***" in caplog.text
        assert "secret-token-value" not in caplog.text

    def test_httpx_logger_does_not_leak_token(self, httpx_mock: HTTPXMock, caplog):
        httpx_mock.add_response(
            json={
                "status": "success",
                "data": {
                    "version": "4.0.0",
                    "prereleaseVersion": None,
                    "buildVersion": "build12",
                    "platform": "win32",
                },
            },
        )

        client = EagleClient(token="secret-token-value")

        with caplog.at_level(logging.INFO, logger="httpx"):
            client.application.info()

        assert "secret-token-value" not in caplog.text

    def test_logs_request_and_response(self, httpx_mock: HTTPXMock, caplog):
        httpx_mock.add_response(json={"status": "success"})

        client = EagleClient(token="my-token")

        with caplog.at_level(logging.INFO, logger="eagle_sdk.http"):
            client.item.add_from_url(url="https://example.com/img.png", name="Test")

        assert "HTTP Request:" in caplog.text
        assert "HTTP Response:" in caplog.text
        assert "my-token" not in caplog.text
