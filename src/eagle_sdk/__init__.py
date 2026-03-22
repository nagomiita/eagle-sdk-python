"""Eagle SDK - Python wrapper for Eagle API."""

from eagle_sdk.client import EagleClient
from eagle_sdk.exceptions import EagleApiError, EagleConnectionError, EagleError
from eagle_sdk.models import (
    AddItemFromPathParam,
    AddItemFromUrlParam,
    ApplicationInfo,
    Folder,
    FolderListItem,
    ItemDetail,
    LibraryInfo,
    Palette,
    TagGroupInfo,
    TagInfo,
)

__all__ = [
    "EagleClient",
    "EagleError",
    "EagleConnectionError",
    "EagleApiError",
    "ApplicationInfo",
    "Palette",
    "ItemDetail",
    "Folder",
    "FolderListItem",
    "LibraryInfo",
    "TagInfo",
    "TagGroupInfo",
    "AddItemFromUrlParam",
    "AddItemFromPathParam",
]
