# eagle-sdk-python 仕様書

## 概要

Eagle APIのPythonラッパーライブラリ。`http://localhost:41595` で動作するEagleのローカルAPIに対して、Pythonから型安全かつ直感的にアクセスできるSDKを提供する。

## 設計方針

- **同期API**: `httpx` を使用した同期クライアント（シンプルさ優先）
- **名前空間パターン**: `client.item.xxx()`, `client.folder.xxx()` のようにリソースごとにグループ化
- **Pythonic命名**: APIのcamelCaseをsnake_caseに変換（例: `addFromURL` → `add_from_url`）
- **型ヒント**: 全メソッドに型アノテーションを付与
- **データクラスによるレスポンス**: APIレスポンスをdataclassでラップし、属性アクセスを提供
- **最小限の依存**: `httpx` のみを外部依存とする

## パッケージ構成

```
eagle_sdk/
├── __init__.py          # EagleClient をエクスポート
├── client.py            # EagleClient 本体
├── http.py              # HTTP通信層（httpx ラッパー）
├── exceptions.py        # 例外クラス定義
├── models.py            # レスポンス用 dataclass
├── api/
│   ├── __init__.py
│   ├── application.py   # ApplicationAPI
│   ├── item.py          # ItemAPI
│   ├── folder.py        # FolderAPI
│   └── library.py       # LibraryAPI
tests/
├── __init__.py
├── test_client.py
├── test_application.py
├── test_item.py
├── test_folder.py
└── test_library.py
pyproject.toml
```

## クラス設計

### EagleClient

```python
class EagleClient:
    def __init__(self, base_url: str = "http://localhost:41595", timeout: float = 30.0):
        ...

    @property
    def application(self) -> ApplicationAPI: ...

    @property
    def item(self) -> ItemAPI: ...

    @property
    def folder(self) -> FolderAPI: ...

    @property
    def library(self) -> LibraryAPI: ...
```

### HttpClient（内部クラス）

```python
class HttpClient:
    def __init__(self, base_url: str, timeout: float): ...
    def get(self, path: str, params: dict | None = None) -> dict: ...
    def post(self, path: str, json: dict | None = None) -> dict: ...
```

- レスポンスの `status` フィールドを検査し、`"success"` でなければ `EagleApiError` を送出
- 接続失敗時は `EagleConnectionError` を送出

### 例外クラス

```python
class EagleError(Exception): ...           # 基底例外
class EagleConnectionError(EagleError): ... # Eagle未起動/接続不可
class EagleApiError(EagleError): ...        # APIがエラーを返した
```

## APIメソッド一覧

### ApplicationAPI

| メソッド | 引数 | 戻り値 | API |
|---------|------|--------|-----|
| `info()` | なし | `ApplicationInfo` | `GET /api/application/info` |

### ItemAPI

| メソッド | 主要引数 | 戻り値 | API |
|---------|---------|--------|-----|
| `add_from_url(url, name, ...)` | url: str, name: str, website?, tags?, star?, annotation?, modification_time?, folder_id?, headers? | `None` | `POST /api/item/addFromURL` |
| `add_from_urls(items, folder_id?)` | items: list[AddItemFromUrlParam], folder_id? | `None` | `POST /api/item/addFromURLs` |
| `add_from_path(path, name, ...)` | path: str, name: str, website?, annotation?, tags?, folder_id? | `None` | `POST /api/item/addFromPath` |
| `add_from_paths(items, folder_id?)` | items: list[AddItemFromPathParam], folder_id? | `None` | `POST /api/item/addFromPaths` |
| `add_bookmark(url, name, ...)` | url: str, name: str, base64?, tags?, modification_time?, folder_id? | `None` | `POST /api/item/addBookmark` |
| `info(id)` | id: str | `ItemDetail` | `GET /api/item/info` |
| `thumbnail(id)` | id: str | `str` | `GET /api/item/thumbnail` |
| `update(id, ...)` | id: str, tags?, annotation?, url?, star? | `ItemDetail` | `POST /api/item/update` |
| `list(...)` | limit?, offset?, order_by?, keyword?, ext?, tags?, folders? | `list[ItemDetail]` | `GET /api/item/list` |
| `move_to_trash(item_ids)` | item_ids: list[str] | `None` | `POST /api/item/moveToTrash` |
| `refresh_palette(id)` | id: str | `None` | `POST /api/item/refreshPalette` |
| `refresh_thumbnail(id)` | id: str | `None` | `POST /api/item/refreshThumbnail` |

### FolderAPI

| メソッド | 主要引数 | 戻り値 | API |
|---------|---------|--------|-----|
| `create(folder_name, parent?)` | folder_name: str, parent? | `Folder` | `POST /api/folder/create` |
| `rename(folder_id, new_name)` | folder_id: str, new_name: str | `Folder` | `POST /api/folder/rename` |
| `update(folder_id, ...)` | folder_id: str, new_name?, new_description?, new_color? | `Folder` | `POST /api/folder/update` |
| `list()` | なし | `list[FolderListItem]` | `GET /api/folder/list` |
| `list_recent()` | なし | `list[FolderListItem]` | `GET /api/folder/listRecent` |

### LibraryAPI

| メソッド | 主要引数 | 戻り値 | API |
|---------|---------|--------|-----|
| `info()` | なし | `LibraryInfo` | `GET /api/library/info` |
| `history()` | なし | `list[str]` | `GET /api/library/history` |
| `switch(library_path)` | library_path: str | `None` | `POST /api/library/switch` |
| `icon(library_path)` | library_path: str | `bytes` | `GET /api/library/icon` |

## データモデル（dataclass）

```python
@dataclass
class ApplicationInfo:
    version: str
    prerelease_version: str | None
    build_version: str
    exec_path: str
    platform: str

@dataclass
class Palette:
    color: list[int]   # [R, G, B]
    ratio: float

@dataclass
class ItemDetail:
    id: str
    name: str
    size: int
    ext: str
    tags: list[str]
    folders: list[str]
    is_deleted: bool
    url: str
    annotation: str
    modification_time: int
    width: int
    height: int
    no_thumbnail: bool
    last_modified: int
    palettes: list[Palette]
    star: int | None = None

@dataclass
class Folder:
    id: str
    name: str
    images: list
    folders: list
    modification_time: int
    tags: list[str]
    children: list
    is_expand: bool

@dataclass
class FolderListItem:
    id: str
    name: str
    description: str
    children: list
    modification_time: int
    tags: list[str]
    image_count: int
    descendant_image_count: int
    pinyin: str
    extend_tags: list[str]

@dataclass
class LibraryInfo:
    folders: list[dict]
    smart_folders: list[dict]
    quick_access: list[dict]
    tags_groups: list[dict]
    modification_time: int
    application_version: str
```

## パラメータ用TypedDict

```python
class AddItemFromUrlParam(TypedDict, total=False):
    url: Required[str]
    name: Required[str]
    website: str
    tags: list[str]
    annotation: str
    modification_time: int
    headers: dict[str, str]

class AddItemFromPathParam(TypedDict, total=False):
    path: Required[str]
    name: Required[str]
    website: str
    tags: list[str]
    annotation: str
```

## camelCase → snake_case 変換ルール

APIのJSONフィールド名（camelCase）は、データモデル上ではsnake_caseに変換する。

| API (camelCase) | Python (snake_case) |
|----------------|---------------------|
| modificationTime | modification_time |
| folderId | folder_id |
| isDeleted | is_deleted |
| noThumbnail | no_thumbnail |
| lastModified | last_modified |
| imageCount | image_count |
| descendantImageCount | descendant_image_count |
| extendTags | extend_tags |
| folderName | folder_name |
| newName | new_name |
| newDescription | new_description |
| newColor | new_color |
| libraryPath | library_path |
| itemIds | item_ids |
| prereleaseVersion | prerelease_version |
| buildVersion | build_version |
| execPath | exec_path |
| isExpand | is_expand |
| smartFolders | smart_folders |
| quickAccess | quick_access |
| tagsGroups | tags_groups |
| applicationVersion | application_version |

## パッケージング

- パッケージマネージャー: `uv`
- ビルドシステム: `hatchling`
- Python: >= 3.10
- 依存: `httpx >= 0.27`
- 開発依存: `pytest`, `pytest-httpx`（httpxのモック）
- ライセンス: MIT

### uv によるプロジェクト管理

```bash
# プロジェクト初期化
uv init

# 依存追加
uv add httpx

# 開発依存追加
uv add --dev pytest pytest-httpx

# テスト実行
uv run pytest

# パッケージビルド
uv build
```
