from __future__ import annotations

from typing import TYPE_CHECKING

from eagle_sdk.models import ApplicationInfo

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


class ApplicationAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def info(self) -> ApplicationInfo:
        resp = self._http.get("/api/application/info")
        return ApplicationInfo.from_dict(resp["data"])
