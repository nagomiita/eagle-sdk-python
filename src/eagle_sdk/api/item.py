from __future__ import annotations

from typing import TYPE_CHECKING, Any

from eagle_sdk.models import AddItemFromPathParam, AddItemFromUrlParam, ItemDetail

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


def _build_item_url_body(param: AddItemFromUrlParam) -> dict[str, Any]:
    body: dict[str, Any] = {"url": param["url"], "name": param["name"]}
    for key in ("website", "tags", "annotation", "headers"):
        if key in param:
            body[key] = param[key]
    if "modification_time" in param:
        body["modificationTime"] = param["modification_time"]
    return body


def _build_item_path_body(param: AddItemFromPathParam) -> dict[str, Any]:
    body: dict[str, Any] = {"path": param["path"], "name": param["name"]}
    for key in ("website", "tags", "annotation"):
        if key in param:
            body[key] = param[key]
    return body


class ItemAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def add_from_url(
        self,
        url: str,
        name: str,
        *,
        website: str | None = None,
        tags: list[str] | None = None,
        star: int | None = None,
        annotation: str | None = None,
        modification_time: int | None = None,
        folder_id: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        body: dict[str, Any] = {"url": url, "name": name}
        if website is not None:
            body["website"] = website
        if tags is not None:
            body["tags"] = tags
        if star is not None:
            body["star"] = star
        if annotation is not None:
            body["annotation"] = annotation
        if modification_time is not None:
            body["modificationTime"] = modification_time
        if folder_id is not None:
            body["folderId"] = folder_id
        if headers is not None:
            body["headers"] = headers
        self._http.post("/api/item/addFromURL", json=body)

    def add_from_urls(
        self,
        items: list[AddItemFromUrlParam],
        *,
        folder_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {
            "items": [_build_item_url_body(item) for item in items],
        }
        if folder_id is not None:
            body["folderId"] = folder_id
        self._http.post("/api/item/addFromURLs", json=body)

    def add_from_path(
        self,
        path: str,
        name: str,
        *,
        website: str | None = None,
        annotation: str | None = None,
        tags: list[str] | None = None,
        folder_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {"path": path, "name": name}
        if website is not None:
            body["website"] = website
        if annotation is not None:
            body["annotation"] = annotation
        if tags is not None:
            body["tags"] = tags
        if folder_id is not None:
            body["folderId"] = folder_id
        self._http.post("/api/item/addFromPath", json=body)

    def add_from_paths(
        self,
        items: list[AddItemFromPathParam],
        *,
        folder_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {
            "items": [_build_item_path_body(item) for item in items],
        }
        if folder_id is not None:
            body["folderId"] = folder_id
        self._http.post("/api/item/addFromPaths", json=body)

    def add_bookmark(
        self,
        url: str,
        name: str,
        *,
        base64: str | None = None,
        tags: list[str] | None = None,
        modification_time: int | None = None,
        folder_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {"url": url, "name": name}
        if base64 is not None:
            body["base64"] = base64
        if tags is not None:
            body["tags"] = tags
        if modification_time is not None:
            body["modificationTime"] = modification_time
        if folder_id is not None:
            body["folderId"] = folder_id
        self._http.post("/api/item/addBookmark", json=body)

    def info(self, id: str) -> ItemDetail:
        resp = self._http.get("/api/item/info", params={"id": id})
        return ItemDetail.from_dict(resp["data"])

    def thumbnail(self, id: str) -> str:
        resp = self._http.get("/api/item/thumbnail", params={"id": id})
        return resp["data"]

    def update(
        self,
        id: str,
        *,
        tags: list[str] | None = None,
        annotation: str | None = None,
        url: str | None = None,
        star: int | None = None,
        folders: list[str] | None = None,
    ) -> ItemDetail:
        body: dict[str, Any] = {"id": id}
        if tags is not None:
            body["tags"] = tags
        if annotation is not None:
            body["annotation"] = annotation
        if url is not None:
            body["url"] = url
        if star is not None:
            body["star"] = star
        if folders is not None:
            body["folders"] = folders
        resp = self._http.post("/api/v2/item/update", json=body)
        return ItemDetail.from_dict(resp["data"])

    def query(
        self,
        keyword: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[ItemDetail]:
        body: dict[str, Any] = {"keyword": keyword}
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        resp = self._http.post("/api/v2/item/query", json=body)
        return [ItemDetail.from_dict(item) for item in resp["data"]]

    def count_all(self) -> int:
        resp = self._http.get("/api/v2/item/countAll")
        return resp["data"]

    def set_custom_thumbnail(self, id: str, path: str) -> None:
        self._http.post(
            "/api/v2/item/setCustomThumbnail",
            json={"id": id, "path": path},
        )

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
        keyword: str | None = None,
        ext: str | None = None,
        tags: str | None = None,
        folders: str | None = None,
    ) -> list[ItemDetail]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if order_by is not None:
            params["orderBy"] = order_by
        if keyword is not None:
            params["keyword"] = keyword
        if ext is not None:
            params["ext"] = ext
        if tags is not None:
            params["tags"] = tags
        if folders is not None:
            params["folders"] = folders
        resp = self._http.get("/api/item/list", params=params or None)
        return [ItemDetail.from_dict(item) for item in resp["data"]]

    def move_to_trash(self, item_ids: list[str]) -> None:
        self._http.post("/api/item/moveToTrash", json={"itemIds": item_ids})

    def refresh_palette(self, id: str) -> None:
        self._http.post("/api/item/refreshPalette", json={"id": id})

    def refresh_thumbnail(self, id: str) -> None:
        self._http.post("/api/item/refreshThumbnail", json={"id": id})
