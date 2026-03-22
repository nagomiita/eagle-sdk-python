from __future__ import annotations

from typing import TYPE_CHECKING, Any

from eagle_sdk.models import TagGroupInfo

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


class TagGroupAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> list[TagGroupInfo]:
        resp = self._http.get("/api/v2/tagGroup/get")
        return [TagGroupInfo.from_dict(g) for g in resp["data"]]

    def create(self, name: str, *, color: str | None = None) -> TagGroupInfo:
        body: dict[str, Any] = {"name": name}
        if color is not None:
            body["color"] = color
        resp = self._http.post("/api/v2/tagGroup/create", json=body)
        return TagGroupInfo.from_dict(resp["data"])

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        color: str | None = None,
    ) -> None:
        body: dict[str, Any] = {"id": id}
        if name is not None:
            body["name"] = name
        if color is not None:
            body["color"] = color
        self._http.post("/api/v2/tagGroup/update", json=body)

    def remove(self, id: str) -> None:
        self._http.post("/api/v2/tagGroup/remove", json={"id": id})

    def add_tags(self, id: str, tags: list[str]) -> None:
        self._http.post(
            "/api/v2/tagGroup/addTags",
            json={"id": id, "tags": tags},
        )

    def remove_tags(self, id: str, tags: list[str]) -> None:
        self._http.post(
            "/api/v2/tagGroup/removeTags",
            json={"id": id, "tags": tags},
        )
