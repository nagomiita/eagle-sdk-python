from __future__ import annotations

import logging
import re
from typing import Any

import httpx

from eagle_sdk.exceptions import EagleApiError, EagleConnectionError

logger = logging.getLogger("eagle_sdk.http")

_TOKEN_RE = re.compile(r"([?&])token=[^&]*")


def _mask_token_in_url(url: httpx.URL | str) -> str:
    return _TOKEN_RE.sub(r"\1token=***", str(url))


def _mask_log_arg(arg: Any) -> Any:
    s = str(arg)
    if _TOKEN_RE.search(s):
        return _TOKEN_RE.sub(r"\1token=***", s)
    return arg


class _TokenMaskingFilter(logging.Filter):
    """Safety-net filter: masks ``token=...`` in log args even when
    the httpx logger is explicitly re-enabled by user code."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(_mask_log_arg(a) for a in record.args)
            elif isinstance(record.args, dict):
                record.args = {k: _mask_log_arg(v) for k, v in record.args.items()}
        return True


def _log_request(request: httpx.Request) -> None:
    logger.info("HTTP Request: %s %s", request.method, _mask_token_in_url(request.url))


def _log_response(response: httpx.Response) -> None:
    logger.info(
        "HTTP Response: %s %s %d",
        response.request.method,
        _mask_token_in_url(response.request.url),
        response.status_code,
    )


class HttpClient:
    def __init__(self, base_url: str, timeout: float, token: str | None = None) -> None:
        params: dict[str, str] | None = None
        event_hooks: dict[str, list[Any]] = {}
        if token:
            params = {"token": token}
            httpx_logger = logging.getLogger("httpx")
            httpx_logger.setLevel(logging.WARNING)
            httpx_logger.addFilter(_TokenMaskingFilter())
            event_hooks = {
                "request": [_log_request],
                "response": [_log_response],
            }
        self._client = httpx.Client(
            base_url=base_url, timeout=timeout, params=params,
            event_hooks=event_hooks,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def get_bytes(self, path: str, params: dict[str, Any] | None = None) -> bytes:
        try:
            response = self._client.get(path, params=params)
            response.raise_for_status()
            return response.content
        except httpx.ConnectError as e:
            raise EagleConnectionError(
                "Cannot connect to Eagle. Is the app running?"
            ) from e

    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=json)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._client.request(method, path, params=params, json=json)
            response.raise_for_status()
        except httpx.ConnectError as e:
            raise EagleConnectionError(
                "Cannot connect to Eagle. Is the app running?"
            ) from e

        data: dict[str, Any] = response.json()
        if data.get("status") != "success":
            raise EagleApiError(data.get("status", "unknown"))
        return data

    def close(self) -> None:
        self._client.close()
