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
