import logging

import httpx
import pytest
from pytest_httpx import HTTPXMock

from eagle_sdk import (
    EagleApiError,
    EagleClient,
    EagleConnectionError,
    EagleTimeoutError,
)
from eagle_sdk.http import _TokenMaskingFilter


class TestTransportErrors:
    def test_timeout_raises_eagle_timeout_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_exception(httpx.ReadTimeout("timed out"))

        client = EagleClient()
        with pytest.raises(EagleTimeoutError):
            client.application.info()

    def test_connect_timeout_raises_eagle_timeout_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_exception(httpx.ConnectTimeout("timed out"))

        client = EagleClient()
        with pytest.raises(EagleTimeoutError):
            client.application.info()

    def test_timeout_error_is_connection_error(self):
        # 既存の except EagleConnectionError がタイムアウトも捕捉できること
        assert issubclass(EagleTimeoutError, EagleConnectionError)

    def test_connect_error_raises_eagle_connection_error(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_exception(httpx.ConnectError("connection refused"))

        client = EagleClient()
        with pytest.raises(EagleConnectionError):
            client.application.info()

    def test_get_bytes_timeout_raises_eagle_timeout_error(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_exception(httpx.ReadTimeout("timed out"))

        client = EagleClient()
        with pytest.raises(EagleTimeoutError):
            client.library.icon("/path/to/library")


class TestHttpStatusErrors:
    def test_401_raises_eagle_api_error_with_status_code(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(status_code=401)

        client = EagleClient(token="secret-token-value")
        with pytest.raises(EagleApiError) as exc_info:
            client.application.info()

        assert exc_info.value.status == "http_error"
        assert exc_info.value.status_code == 401

    def test_status_error_does_not_leak_token(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=401)

        client = EagleClient(token="secret-token-value")
        with pytest.raises(EagleApiError) as exc_info:
            client.application.info()

        assert "secret-token-value" not in str(exc_info.value)
        assert "token=***" in str(exc_info.value)
        # httpx.HTTPStatusError (token 入り URL を含む) をチェーンしていないこと
        assert exc_info.value.__cause__ is None

    def test_get_bytes_status_error_raises_eagle_api_error(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(status_code=404)

        client = EagleClient()
        with pytest.raises(EagleApiError) as exc_info:
            client.library.icon("/path/to/library")

        assert exc_info.value.status_code == 404


class TestApiLevelErrors:
    def test_error_status_raises_with_message(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"status": "error", "message": "Folder not found"},
        )

        client = EagleClient()
        with pytest.raises(EagleApiError) as exc_info:
            client.folder.list()

        assert exc_info.value.status == "error"
        assert "Folder not found" in str(exc_info.value)
        assert exc_info.value.data == {
            "status": "error",
            "message": "Folder not found",
        }

    def test_error_status_without_message(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"status": "error"})

        client = EagleClient()
        with pytest.raises(EagleApiError) as exc_info:
            client.folder.list()

        assert exc_info.value.status == "error"
        assert "Eagle API error: error" in str(exc_info.value)

    def test_non_json_response_raises_eagle_api_error(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(content=b"<html>Bad Gateway</html>")

        client = EagleClient()
        with pytest.raises(EagleApiError) as exc_info:
            client.folder.list()

        assert exc_info.value.status == "invalid_response"


class TestHttpxLoggerSideEffects:
    def test_masking_filter_installed_only_once(self, httpx_mock: HTTPXMock):
        httpx_logger = logging.getLogger("httpx")
        for f in list(httpx_logger.filters):
            if isinstance(f, _TokenMaskingFilter):
                httpx_logger.removeFilter(f)

        for _ in range(100):
            EagleClient(token="secret-token-value")

        count = sum(
            isinstance(f, _TokenMaskingFilter) for f in httpx_logger.filters
        )
        assert count == 1

    def test_httpx_logger_level_not_modified(self, httpx_mock: HTTPXMock):
        httpx_logger = logging.getLogger("httpx")
        original_level = httpx_logger.level

        EagleClient(token="secret-token-value")

        assert httpx_logger.level == original_level
