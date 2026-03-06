from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
        body: dict[str, Any] = {"folderName": folder_name}
        if parent is not None:
            body["parent"] = parent
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
        body: dict[str, Any] = {"folderId": folder_id}
        if new_name is not None:
            body["newName"] = new_name
        if new_description is not None:
            body["newDescription"] = new_description
        if new_color is not None:
            body["newColor"] = new_color
        resp = self._http.post("/api/folder/update", json=body)
        return Folder.from_dict(resp["data"])

    def list(self) -> list[FolderListItem]:
        resp = self._http.get("/api/folder/list")
        return [FolderListItem.from_dict(f) for f in resp["data"]]

    def list_recent(self) -> list[FolderListItem]:
        resp = self._http.get("/api/folder/listRecent")
        return [FolderListItem.from_dict(f) for f in resp["data"]]
