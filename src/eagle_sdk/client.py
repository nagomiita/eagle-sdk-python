from __future__ import annotations

from eagle_sdk.api.application import ApplicationAPI
from eagle_sdk.api.folder import FolderAPI
from eagle_sdk.api.item import ItemAPI
from eagle_sdk.api.library import LibraryAPI
from eagle_sdk.http import HttpClient


class EagleClient:
    def __init__(
        self,
        base_url: str = "http://localhost:41595",
        timeout: float = 30.0,
    ) -> None:
        self._http = HttpClient(base_url=base_url, timeout=timeout)
        self._application = ApplicationAPI(self._http)
        self._item = ItemAPI(self._http)
        self._folder = FolderAPI(self._http)
        self._library = LibraryAPI(self._http)

    @property
    def application(self) -> ApplicationAPI:
        return self._application

    @property
    def item(self) -> ItemAPI:
        return self._item

    @property
    def folder(self) -> FolderAPI:
        return self._folder

    @property
    def library(self) -> LibraryAPI:
        return self._library

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> EagleClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
