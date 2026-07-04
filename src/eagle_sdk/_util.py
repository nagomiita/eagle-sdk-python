from __future__ import annotations

from functools import lru_cache
from typing import Any


# キーは各 API メソッドの引数名 (固定語彙) なのでヒット率はほぼ 100% (#5)。
@lru_cache(maxsize=1024)
def to_camel_case(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(part.capitalize() for part in rest)


def compact_body(**kwargs: Any) -> dict[str, Any]:
    """None の値を除外し、キーを camelCase へ変換した dict を返す。

    Eagle API へ送る body / query params の「optional 引数ごとの if 連打 +
    camelCase 手書き」を 1 行に畳むためのヘルパー (#5)。
    """
    return {to_camel_case(k): v for k, v in kwargs.items() if v is not None}
