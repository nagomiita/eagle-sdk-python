"""Eagle SDK - Python wrapper for Eagle API."""

from eagle_sdk.client import EagleClient
from eagle_sdk.exceptions import (
    EagleApiError,
    EagleConnectionError,
    EagleError,
    EagleTimeoutError,
)
from eagle_sdk.wsl import resolve_base_url
from eagle_sdk.models import (
    AddItemFromPathParam,
    AddItemResult,
    AddItemsResult,
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
    "EagleTimeoutError",
    "EagleApiError",
    "resolve_base_url",
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
    "AddItemResult",
    "AddItemsResult",
]
