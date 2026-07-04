class TestToSnakeCaseCache:
    def test_cached_after_first_call(self):
        from eagle_sdk.models import _to_snake_case

        _to_snake_case.cache_clear()
        assert _to_snake_case("modificationTime") == "modification_time"
        assert _to_snake_case("modificationTime") == "modification_time"

        info = _to_snake_case.cache_info()
        assert info.hits >= 1
        assert info.misses == 1


class TestFromDictCommon:
    def test_unknown_keys_are_ignored_and_defaults_applied(self):
        from eagle_sdk.models import ItemDetail

        item = ItemDetail.from_dict({"id": "X", "name": "n", "unknownKey": 1})
        assert item.id == "X"
        assert item.size == 0
        assert item.tags == []
        assert item.palettes == []
        assert item.star is None

    def test_default_lists_are_not_shared(self):
        from eagle_sdk.models import ItemDetail

        a = ItemDetail.from_dict({"id": "A", "name": "a"})
        b = ItemDetail.from_dict({"id": "B", "name": "b"})
        a.tags.append("t")
        assert b.tags == []
