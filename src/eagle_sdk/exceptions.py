from __future__ import annotations

from typing import Any


class EagleError(Exception):
    """Base exception for Eagle SDK."""


class EagleConnectionError(EagleError):
    """Raised when connection to Eagle API fails."""


class EagleTimeoutError(EagleConnectionError):
    """Raised when a request to Eagle API times out."""


class EagleApiError(EagleError):
    """Raised when Eagle API returns an error response.

    Covers three cases:

    - API-level error body (``{"status": "error", ...}``)
    - HTTP status error (4xx / 5xx) — ``status`` is ``"http_error"``
    - non-JSON response — ``status`` is ``"invalid_response"``

    :param status: Eagle API の ``status`` フィールド、または SDK が割り当てる分類子
    :param message: 例外メッセージ (省略時は ``Eagle API error: {status}``)
    :param status_code: HTTP ステータスコード (取得できた場合)
    :param data: Eagle API が返した生のレスポンスボディ (dict の場合)
    """

    def __init__(
        self,
        status: str,
        message: str = "",
        *,
        status_code: int | None = None,
        data: Any = None,
    ):
        self.status = status
        self.status_code = status_code
        self.data = data
        super().__init__(message or f"Eagle API error: {status}")
