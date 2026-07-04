from eagle_sdk._util import compact_body, to_camel_case


class TestToCamelCase:
    def test_converts_snake_case(self):
        assert to_camel_case("modification_time") == "modificationTime"
        assert to_camel_case("folder_id") == "folderId"
        assert to_camel_case("new_description") == "newDescription"

    def test_passes_through_single_word(self):
        assert to_camel_case("url") == "url"
        assert to_camel_case("base64") == "base64"


class TestCompactBody:
    def test_drops_none_and_converts_keys(self):
        body = compact_body(url="u", folder_id="f", star=None, tags=None)
        assert body == {"url": "u", "folderId": "f"}

    def test_keeps_falsy_non_none_values(self):
        body = compact_body(star=0, tags=[], annotation="")
        assert body == {"star": 0, "tags": [], "annotation": ""}
