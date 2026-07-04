from __future__ import annotations

import logging
import re
from typing import Any

import httpx

from eagle_sdk.exceptions import (
    EagleApiError,
    EagleConnectionError,
    EagleTimeoutError,
)

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


def _ensure_httpx_token_masking() -> None:
    """httpx logger に token マスクフィルタを 1 度だけ登録する。

    ``logging.getLogger("httpx")`` はプロセス内シングルトンのため、クライアント
    生成のたびに ``addFilter`` すると filter インスタンスが累積する (#2)。
    既登録なら何もしない。``setLevel`` はプロセス全体の httpx ログ設定を変える
    global 副作用になるため行わない (httpx 自身の INFO ログもこの filter で
    マスクされる)。
    """
    httpx_logger = logging.getLogger("httpx")
    if not any(isinstance(f, _TokenMaskingFilter) for f in httpx_logger.filters):
        httpx_logger.addFilter(_TokenMaskingFilter())


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
            _ensure_httpx_token_masking()
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
        return self._send("GET", path, params=params).content

    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=json)

    def _send(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """リクエストを送信し、transport / HTTP ステータス起因の失敗を
        SDK 例外 (``EagleError`` 系) に変換して返す。"""
        try:
            response = self._client.request(method, path, params=params, json=json)
        except httpx.TimeoutException as e:
            raise EagleTimeoutError(
                f"Request to Eagle timed out: {method} {path}"
            ) from e
        except httpx.ConnectError as e:
            raise EagleConnectionError(
                "Cannot connect to Eagle. Is the app running?"
            ) from e

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            # httpx.HTTPStatusError の str には ?token=... 入りの完全 URL が
            # 含まれるため、チェーンせずマスク済みメッセージで raise する
            raise EagleApiError(
                "http_error",
                f"Eagle API returned HTTP {response.status_code}"
                f" {response.reason_phrase}:"
                f" {method} {_mask_token_in_url(response.request.url)}",
                status_code=response.status_code,
            ) from None
        return response

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self._send(method, path, params=params, json=json)

        try:
            data: dict[str, Any] = response.json()
        except ValueError as e:
            raise EagleApiError(
                "invalid_response",
                f"Eagle API returned a non-JSON response"
                f" (HTTP {response.status_code}): {method} {path}",
                status_code=response.status_code,
            ) from e

        if data.get("status") != "success":
            status = data.get("status", "unknown")
            detail = data.get("message") or data.get("data")
            message = f"Eagle API error: {status}"
            if detail:
                message = f"{message} - {detail}"
            raise EagleApiError(
                status,
                message,
                status_code=response.status_code,
                data=data,
            )
        return data

    def close(self) -> None:
        self._client.close()
