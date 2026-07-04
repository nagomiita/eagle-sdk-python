class TestToSnakeCaseCache:
    def test_cached_after_first_call(self):
        from eagle_sdk.models import _to_snake_case

        _to_snake_case.cache_clear()
        assert _to_snake_case("modificationTime") == "modification_time"
        assert _to_snake_case("modificationTime") == "modification_time"

        info = _to_snake_case.cache_info()
        assert info.hits >= 1
        assert info.misses == 1
