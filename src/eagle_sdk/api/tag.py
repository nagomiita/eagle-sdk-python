from __future__ import annotations

from typing import TYPE_CHECKING, Any

from eagle_sdk.models import TagInfo

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


class TagAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, *, keyword: str | None = None) -> list[TagInfo]:
        params: dict[str, Any] = {}
        if keyword is not None:
            params["keyword"] = keyword
        resp = self._http.get("/api/v2/tag/get", params=params or None)
        return [TagInfo.from_dict(t) for t in resp["data"]]

    def get_recent(self) -> list[TagInfo]:
        resp = self._http.get("/api/v2/tag/getRecentTags")
        return [TagInfo.from_dict(t) for t in resp["data"]]

    def get_starred(self) -> list[TagInfo]:
        resp = self._http.get("/api/v2/tag/getStarredTags")
        return [TagInfo.from_dict(t) for t in resp["data"]]

    def update(self, tag_name: str, new_name: str) -> None:
        self._http.post(
            "/api/v2/tag/update",
            json={"name": tag_name, "newName": new_name},
        )

    def merge(self, from_tags: list[str], to_tag: str) -> None:
        self._http.post(
            "/api/v2/tag/merge",
            json={"fromTags": from_tags, "toTag": to_tag},
        )
