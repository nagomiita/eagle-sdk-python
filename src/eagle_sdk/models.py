from __future__ import annotations

import re
from dataclasses import dataclass, field, fields
from functools import lru_cache
from typing import Any, Required, TypedDict, TypeVar


# キーは API レスポンスの固定語彙 (modificationTime 等の十数種) なので
# ヒット率はほぼ 100%。大量アイテムのデシリアライズで regex 評価を
# 初回のみにする (#4)。
@lru_cache(maxsize=1024)
def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def _convert_keys(data: dict[str, Any]) -> dict[str, Any]:
    return {_to_snake_case(k): v for k, v in data.items()}


_T = TypeVar("_T", bound="_FromDict")


class _FromDict:
    """レスポンス dict → dataclass の共通変換 (#5)。

    トップレベルキーを snake_case 化し、dataclass に定義されたフィールド
    だけを拾って構築する。欠損キーのデフォルトはフィールド定義側に一元化
    する (from_dict 側での d.get(..., default) 二重管理をなくす)。
    """

    @classmethod
    def from_dict(cls: type[_T], data: dict[str, Any]) -> _T:
        d = _convert_keys(data)
        names = {f.name for f in fields(cls)}  # type: ignore[arg-type]
        return cls(**{k: v for k, v in d.items() if k in names})


# ──────────────────────────────────────────────
# Application
# ──────────────────────────────────────────────


@dataclass
class ApplicationInfo(_FromDict):
    version: str
    platform: str
    prerelease_version: str | None = None
    build_version: str = ""
    exec_path: str | None = None


# ──────────────────────────────────────────────
# Item
# ──────────────────────────────────────────────


@dataclass
class Palette(_FromDict):
    color: list[int]
    ratio: float


@dataclass
class ItemDetail(_FromDict):
    id: str
    name: str
    size: int = 0
    ext: str = ""
    tags: list[str] = field(default_factory=list)
    folders: list[str] = field(default_factory=list)
    is_deleted: bool = False
    url: str = ""
    annotation: str = ""
    modification_time: int = 0
    width: int = 0
    height: int = 0
    no_thumbnail: bool = False
    last_modified: int = 0
    palettes: list[Palette] = field(default_factory=list)
    star: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ItemDetail:
        data = {
            **data,
            "palettes": [Palette.from_dict(p) for p in data.get("palettes", [])],
        }
        return super().from_dict(data)


@dataclass
class AddItemResult(_FromDict):
    id: str


@dataclass
class AddItemsResult(_FromDict):
    ids: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────
# Folder
# ──────────────────────────────────────────────


@dataclass
class Folder(_FromDict):
    id: str
    name: str
    images: list[dict[str, Any]] = field(default_factory=list)
    folders: list[dict[str, Any]] = field(default_factory=list)
    modification_time: int = 0
    tags: list[str] = field(default_factory=list)
    children: list[dict[str, Any]] = field(default_factory=list)
    is_expand: bool = False


@dataclass
class FolderListItem(_FromDict):
    id: str
    name: str
    description: str = ""
    children: list[dict[str, Any]] = field(default_factory=list)
    modification_time: int = 0
    tags: list[str] = field(default_factory=list)
    image_count: int = 0
    descendant_image_count: int = 0
    pinyin: str = ""
    extend_tags: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────
# Library
# ──────────────────────────────────────────────


@dataclass
class LibraryInfo(_FromDict):
    folders: list[dict[str, Any]] = field(default_factory=list)
    smart_folders: list[dict[str, Any]] = field(default_factory=list)
    quick_access: list[dict[str, Any]] = field(default_factory=list)
    tags_groups: list[dict[str, Any]] = field(default_factory=list)
    modification_time: int = 0
    application_version: str = ""
    # /api/library/info の data.library から取得する、現在 Eagle が開いている
    # ライブラリのネイティブパスと名前 (古い Eagle がフィールドを返さない場合は None)
    library_path: str | None = None
    library_name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LibraryInfo:
        obj = super().from_dict(data)
        library = data.get("library") or {}
        obj.library_path = library.get("path")
        obj.library_name = library.get("name")
        return obj


# ──────────────────────────────────────────────
# Tag
# ──────────────────────────────────────────────


@dataclass
class TagInfo(_FromDict):
    name: str = ""
    count: int = 0
    starred: bool = False


# ──────────────────────────────────────────────
# Tag Group
# ──────────────────────────────────────────────


@dataclass
class TagGroupInfo(_FromDict):
    id: str
    name: str = ""
    tags: list[str] = field(default_factory=list)
    color: str = ""


# ──────────────────────────────────────────────
# Parameter TypedDicts
# ──────────────────────────────────────────────


class AddItemFromUrlParam(TypedDict, total=False):
    url: Required[str]
    name: Required[str]
    website: str
    tags: list[str]
    star: int
    annotation: str
    modification_time: int
    headers: dict[str, str]


class AddItemFromPathParam(TypedDict, total=False):
    path: Required[str]
    name: Required[str]
    id: str
    website: str
    tags: list[str]
    annotation: str
    folders: list[str]
