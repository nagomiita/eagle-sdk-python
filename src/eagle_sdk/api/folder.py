from __future__ import annotations

from typing import TYPE_CHECKING

from eagle_sdk._util import compact_body
from eagle_sdk.models import Folder, FolderListItem

if TYPE_CHECKING:
    from eagle_sdk.http import HttpClient


class FolderAPI:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        folder_name: str,
        *,
        parent: str | None = None,
    ) -> Folder:
        body = compact_body(folder_name=folder_name, parent=parent)
        resp = self._http.post("/api/folder/create", json=body)
        return Folder.from_dict(resp["data"])

    def rename(self, folder_id: str, new_name: str) -> Folder:
        resp = self._http.post(
            "/api/folder/rename",
            json={"folderId": folder_id, "newName": new_name},
        )
        return Folder.from_dict(resp["data"])

    def update(
        self,
        folder_id: str,
        *,
        new_name: str | None = None,
        new_description: str | None = None,
        new_color: str | None = None,
    ) -> Folder:
        body = compact_body(
            folder_id=folder_id,
            new_name=new_name,
            new_description=new_description,
            new_color=new_color,
        )
        resp = self._http.post("/api/folder/update", json=body)
        return Folder.from_dict(resp["data"])

    def list(self) -> list[FolderListItem]:
        resp = self._http.get("/api/folder/list")
        return [FolderListItem.from_dict(f) for f in resp["data"]]

    def list_recent(self) -> list[FolderListItem]:
        resp = self._http.get("/api/folder/listRecent")
        return [FolderListItem.from_dict(f) for f in resp["data"]]
