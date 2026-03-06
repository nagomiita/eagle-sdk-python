from __future__ import annotations

from typing import Any

import httpx

from eagle_sdk.exceptions import EagleApiError, EagleConnectionError


class HttpClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

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
