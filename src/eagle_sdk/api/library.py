from __future__ import annotations

from typing import TYPE_CHECKING

from eagle_sdk.models import LibraryInfo

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


class LibraryAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def info(self) -> LibraryInfo:
        resp = self._http.get("/api/library/info")
        return LibraryInfo.from_dict(resp["data"])

    def history(self) -> list[str]:
        resp = self._http.get("/api/library/history")
        return resp["data"]

    def switch(self, library_path: str) -> None:
        self._http.post("/api/library/switch", json={"libraryPath": library_path})

    def icon(self, library_path: str) -> bytes:
        return self._http.get_bytes(
            "/api/library/icon", params={"libraryPath": library_path}
        )
