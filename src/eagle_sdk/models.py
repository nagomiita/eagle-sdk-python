from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Required, TypedDict


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def _convert_keys(data: dict[str, Any]) -> dict[str, Any]:
    return {_to_snake_case(k): v for k, v in data.items()}


# ──────────────────────────────────────────────
# Application
# ──────────────────────────────────────────────

@dataclass
class ApplicationInfo:
    version: str
    prerelease_version: str | None
    build_version: str
    exec_path: str
    platform: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ApplicationInfo:
        d = _convert_keys(data)
        return cls(
            version=d["version"],
            prerelease_version=d.get("prerelease_version"),
            build_version=d["build_version"],
            exec_path=d["exec_path"],
            platform=d["platform"],
        )


# ──────────────────────────────────────────────
# Item
# ──────────────────────────────────────────────

@dataclass
class Palette:
    color: list[int]
    ratio: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Palette:
        return cls(color=data["color"], ratio=data["ratio"])


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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ItemDetail:
        d = _convert_keys(data)
        return cls(
            id=d["id"],
            name=d["name"],
            size=d.get("size", 0),
            ext=d.get("ext", ""),
            tags=d.get("tags", []),
            folders=d.get("folders", []),
            is_deleted=d.get("is_deleted", False),
            url=d.get("url", ""),
            annotation=d.get("annotation", ""),
            modification_time=d.get("modification_time", 0),
            width=d.get("width", 0),
            height=d.get("height", 0),
            no_thumbnail=d.get("no_thumbnail", False),
            last_modified=d.get("last_modified", 0),
            palettes=[Palette.from_dict(p) for p in d.get("palettes", [])],
            star=d.get("star"),
        )


# ──────────────────────────────────────────────
# Folder
# ──────────────────────────────────────────────

@dataclass
class Folder:
    id: str
    name: str
    images: list[Any]
    folders: list[Any]
    modification_time: int
    tags: list[str]
    children: list[Any]
    is_expand: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Folder:
        d = _convert_keys(data)
        return cls(
            id=d["id"],
            name=d["name"],
            images=d.get("images", []),
            folders=d.get("folders", []),
            modification_time=d.get("modification_time", 0),
            tags=d.get("tags", []),
            children=d.get("children", []),
            is_expand=d.get("is_expand", False),
        )


@dataclass
class FolderListItem:
    id: str
    name: str
    description: str
    children: list[Any]
    modification_time: int
    tags: list[str]
    image_count: int
    descendant_image_count: int
    pinyin: str
    extend_tags: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FolderListItem:
        d = _convert_keys(data)
        return cls(
            id=d["id"],
            name=d["name"],
            description=d.get("description", ""),
            children=d.get("children", []),
            modification_time=d.get("modification_time", 0),
            tags=d.get("tags", []),
            image_count=d.get("image_count", 0),
            descendant_image_count=d.get("descendant_image_count", 0),
            pinyin=d.get("pinyin", ""),
            extend_tags=d.get("extend_tags", []),
        )


# ──────────────────────────────────────────────
# Library
# ──────────────────────────────────────────────

@dataclass
class LibraryInfo:
    folders: list[dict[str, Any]]
    smart_folders: list[dict[str, Any]]
    quick_access: list[dict[str, Any]]
    tags_groups: list[dict[str, Any]]
    modification_time: int
    application_version: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LibraryInfo:
        d = _convert_keys(data)
        return cls(
            folders=d.get("folders", []),
            smart_folders=d.get("smart_folders", []),
            quick_access=d.get("quick_access", []),
            tags_groups=d.get("tags_groups", []),
            modification_time=d.get("modification_time", 0),
            application_version=d.get("application_version", ""),
        )


# ──────────────────────────────────────────────
# Parameter TypedDicts
# ──────────────────────────────────────────────

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
