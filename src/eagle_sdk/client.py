from __future__ import annotations

import httpx

from eagle_sdk.api.application import ApplicationAPI
from eagle_sdk.api.folder import FolderAPI
from eagle_sdk.api.item import ItemAPI
from eagle_sdk.api.library import LibraryAPI
from eagle_sdk.api.tag import TagAPI
from eagle_sdk.api.tag_group import TagGroupAPI
from eagle_sdk.http import HttpClient


class EagleClient:
    """Eagle アプリの HTTP API クライアント。

    インスタンスは httpx.Client (TCP コネクションプール) を 1 個保持する。
    リクエストのたびに生成すると keep-alive が効かないため、プロセス内で
    使い回すこと (httpx.Client 準拠でスレッドセーフ)。使い終わったら
    ``close()`` するか、コンテキストマネージャとして使う。

    :param retries: connect レベルのリトライ回数 (``httpx.HTTPTransport(retries=N)``)。
        Eagle 起動直後などの一時的な接続拒否を吸収する opt-in。送信済み
        リクエストの再送はしない。デフォルト 0 (リトライなし)
    :param limits: コネクションプール設定 (``httpx.Limits``)。省略時は httpx 既定値
    """

    def __init__(
        self,
        base_url: str = "http://localhost:41595",
        timeout: float = 30.0,
        token: str | None = None,
        retries: int = 0,
        limits: httpx.Limits | None = None,
    ) -> None:
        self._http = HttpClient(
            base_url=base_url,
            timeout=timeout,
            token=token,
            retries=retries,
            limits=limits,
        )
        self._application = ApplicationAPI(self._http)
        self._item = ItemAPI(self._http)
        self._folder = FolderAPI(self._http)
        self._library = LibraryAPI(self._http)
        self._tag = TagAPI(self._http)
        self._tag_group = TagGroupAPI(self._http)

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

    @property
    def tag(self) -> TagAPI:
        return self._tag

    @property
    def tag_group(self) -> TagGroupAPI:
        return self._tag_group

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> EagleClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
