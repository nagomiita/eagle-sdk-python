from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from eagle_sdk._util import compact_body
from eagle_sdk.models import (
    AddItemFromPathParam,
    AddItemFromUrlParam,
    AddItemResult,
    AddItemsResult,
    ItemDetail,
)

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


def _build_item_url_body(param: AddItemFromUrlParam) -> dict[str, Any]:
    return compact_body(
        url=param["url"],
        name=param["name"],
        website=param.get("website"),
        tags=param.get("tags"),
        star=param.get("star"),
        annotation=param.get("annotation"),
        modification_time=param.get("modification_time"),
        headers=param.get("headers"),
    )


def _resolve_item_folders(
    *,
    folder_id: str | None = None,
    folders: list[str] | None = None,
) -> list[str] | None:
    if folder_id is not None and folders is not None:
        raise ValueError("folder_id and folders cannot be used together")
    if folders is not None:
        return folders
    if folder_id is not None:
        return [folder_id]
    return None


def _build_item_path_body(
    param: AddItemFromPathParam,
    *,
    folder_id: str | None = None,
) -> dict[str, Any]:
    return compact_body(
        path=param["path"],
        name=param["name"],
        id=param.get("id"),
        website=param.get("website"),
        tags=param.get("tags"),
        annotation=param.get("annotation"),
        folders=_resolve_item_folders(
            folder_id=folder_id,
            folders=param.get("folders"),
        ),
    )


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
        body = compact_body(
            url=url,
            name=name,
            website=website,
            tags=tags,
            star=star,
            annotation=annotation,
            modification_time=modification_time,
            folder_id=folder_id,
            headers=headers,
        )
        self._http.post("/api/item/addFromURL", json=body)

    def add_from_urls(
        self,
        items: list[AddItemFromUrlParam],
        *,
        folder_id: str | None = None,
    ) -> None:
        body = compact_body(
            items=[_build_item_url_body(item) for item in items],
            folder_id=folder_id,
        )
        self._http.post("/api/item/addFromURLs", json=body)

    def add_from_path(
        self,
        path: str,
        name: str,
        *,
        id: str | None = None,
        website: str | None = None,
        annotation: str | None = None,
        tags: list[str] | None = None,
        folder_id: str | None = None,
        folders: list[str] | None = None,
    ) -> AddItemResult:
        body = compact_body(
            path=path,
            name=name,
            id=id,
            website=website,
            annotation=annotation,
            tags=tags,
            folders=_resolve_item_folders(folder_id=folder_id, folders=folders),
        )
        resp = self._http.post("/api/v2/item/add", json=body)
        return AddItemResult.from_dict(resp["data"])

    def add_from_paths(
        self,
        items: list[AddItemFromPathParam],
        *,
        folder_id: str | None = None,
    ) -> AddItemsResult:
        body: dict[str, Any] = {
            "items": [
                _build_item_path_body(item, folder_id=folder_id) for item in items
            ],
        }
        resp = self._http.post("/api/v2/item/add", json=body)
        return AddItemsResult.from_dict(resp["data"])

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
        body = compact_body(
            url=url,
            name=name,
            base64=base64,
            tags=tags,
            modification_time=modification_time,
            folder_id=folder_id,
        )
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
        body = compact_body(
            id=id,
            tags=tags,
            annotation=annotation,
            url=url,
            star=star,
            folders=folders,
        )
        resp = self._http.post("/api/v2/item/update", json=body)
        return ItemDetail.from_dict(resp["data"])

    def query(
        self,
        keyword: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[ItemDetail]:
        body = compact_body(keyword=keyword, limit=limit, offset=offset)
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
        params = compact_body(
            limit=limit,
            offset=offset,
            order_by=order_by,
            keyword=keyword,
            ext=ext,
            tags=tags,
            folders=folders,
        )
        resp = self._http.get("/api/item/list", params=params or None)
        return [ItemDetail.from_dict(item) for item in resp["data"]]

    def iter_all(
        self,
        *,
        page_size: int = 200,
        order_by: str | None = None,
        keyword: str | None = None,
        ext: str | None = None,
        tags: str | None = None,
        folders: str | None = None,
    ) -> Iterator[ItemDetail]:
        """条件に一致する item をページングしながら順に yield する (#4)。

        呼び出し側が ``count_all()`` + ``list(limit=total)`` で全件を 1 レスポンス
        に載せる必要をなくす。Eagle API の ``/api/item/list`` の ``offset`` は
        「ページ番号」(``limit`` 単位) の意味論なので、ページ番号を進めながら
        取得し、``page_size`` 未満のページが返ったら終端とみなす。
        """
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        page = 0
        while True:
            items = self.list(
                limit=page_size,
                offset=page,
                order_by=order_by,
                keyword=keyword,
                ext=ext,
                tags=tags,
                folders=folders,
            )
            yield from items
            if len(items) < page_size:
                return
            page += 1

    def move_to_trash(self, item_ids: list[str]) -> None:
        self._http.post("/api/item/moveToTrash", json={"itemIds": item_ids})

    def refresh_palette(self, id: str) -> None:
        self._http.post("/api/item/refreshPalette", json={"id": id})

    def refresh_thumbnail(self, id: str) -> None:
        self._http.post("/api/item/refreshThumbnail", json={"id": id})
