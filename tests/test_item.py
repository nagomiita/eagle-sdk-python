import json

import pytest
from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient, EagleApiError

ITEM_RESPONSE = {
    "id": "KBHG6KA0Y5S9W",
    "name": "Work",
    "size": 45231,
    "ext": "png",
    "tags": ["Design"],
    "folders": [],
    "isDeleted": False,
    "url": "https://example.com",
    "annotation": "",
    "modificationTime": 1591325171766,
    "width": 623,
    "height": 623,
    "noThumbnail": False,
    "lastModified": 1591325171766,
    "palettes": [{"color": [232, 198, 159], "ratio": 34.05}],
    "star": 3,
}


class TestItemAddFromUrl:
    def test_basic(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/addFromURL",
            json={"status": "success"},
        )
        client.item.add_from_url(url="https://example.com/img.png", name="Test")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["url"] == "https://example.com/img.png"
        assert body["name"] == "Test"

    def test_all_params(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/addFromURL",
            json={"status": "success"},
        )
        client.item.add_from_url(
            url="https://example.com/img.png",
            name="Test",
            website="https://example.com",
            tags=["tag1"],
            star=5,
            annotation="note",
            modification_time=12345,
            folder_id="FOLDER1",
            headers={"referer": "example.com"},
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["website"] == "https://example.com"
        assert body["tags"] == ["tag1"]
        assert body["star"] == 5
        assert body["annotation"] == "note"
        assert body["modificationTime"] == 12345
        assert body["folderId"] == "FOLDER1"
        assert body["headers"] == {"referer": "example.com"}


class TestItemAddFromUrls:
    def test_basic(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/addFromURLs",
            json={"status": "success"},
        )
        client.item.add_from_urls(
            [{"url": "https://example.com/1.png", "name": "One"}],
            folder_id="F1",
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert len(body["items"]) == 1
        assert body["items"][0]["url"] == "https://example.com/1.png"
        assert body["folderId"] == "F1"


class TestItemAddFromPath:
    def test_basic(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/add",
            json={"status": "success", "data": {"id": "ITEM1"}},
        )
        result = client.item.add_from_path(path="/tmp/test.jpg", name="Test")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["path"] == "/tmp/test.jpg"
        assert body["name"] == "Test"
        assert result.id == "ITEM1"

    def test_with_custom_id_and_folders(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/add",
            json={"status": "success", "data": {"id": "CUSTOM1"}},
        )
        result = client.item.add_from_path(
            path="/tmp/test.jpg",
            name="Test",
            id="CUSTOM1",
            folders=["F1", "F2"],
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["id"] == "CUSTOM1"
        assert body["folders"] == ["F1", "F2"]
        assert result.id == "CUSTOM1"

    def test_folder_id_is_converted_to_folders(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/add",
            json={"status": "success", "data": {"id": "ITEM2"}},
        )
        client.item.add_from_path(
            path="/tmp/test.jpg",
            name="Test",
            folder_id="FOLDER1",
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["folders"] == ["FOLDER1"]

    def test_folder_id_conflicts_with_folders(self, client: EagleClient):
        with pytest.raises(ValueError):
            client.item.add_from_path(
                path="/tmp/test.jpg",
                name="Test",
                folder_id="FOLDER1",
                folders=["FOLDER2"],
            )


class TestItemAddFromPaths:
    def test_basic(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/add",
            json={"status": "success", "data": {"ids": ["ID1", "ID2"]}},
        )
        result = client.item.add_from_paths(
            [
                {"path": "/tmp/1.jpg", "name": "One"},
                {"path": "/tmp/2.jpg", "name": "Two"},
            ],
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert len(body["items"]) == 2
        assert result.ids == ["ID1", "ID2"]

    def test_folder_id_is_applied_to_each_item(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/add",
            json={"status": "success", "data": {"ids": ["ID1", "ID2"]}},
        )
        client.item.add_from_paths(
            [
                {"path": "/tmp/1.jpg", "name": "One"},
                {"path": "/tmp/2.jpg", "name": "Two"},
            ],
            folder_id="FOLDER1",
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["items"][0]["folders"] == ["FOLDER1"]
        assert body["items"][1]["folders"] == ["FOLDER1"]

    def test_folder_id_conflicts_with_item_folders(self, client: EagleClient):
        with pytest.raises(ValueError):
            client.item.add_from_paths(
                [
                    {
                        "path": "/tmp/1.jpg",
                        "name": "One",
                        "folders": ["FOLDER2"],
                    }
                ],
                folder_id="FOLDER1",
            )


class TestItemAddBookmark:
    def test_basic(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/addBookmark",
            json={"status": "success"},
        )
        client.item.add_bookmark(url="https://example.com", name="Bookmark")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["url"] == "https://example.com"
        assert body["name"] == "Bookmark"


class TestItemInfo:
    def test_info(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/info?id=KBHG6KA0Y5S9W",
            json={"status": "success", "data": ITEM_RESPONSE},
        )

        item = client.item.info("KBHG6KA0Y5S9W")

        assert item.id == "KBHG6KA0Y5S9W"
        assert item.name == "Work"
        assert item.size == 45231
        assert item.width == 623
        assert item.palettes[0].color == [232, 198, 159]
        assert item.star == 3


class TestItemThumbnail:
    def test_thumbnail(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/thumbnail?id=KBHG6KA0Y5S9W",
            json={
                "status": "success",
                "data": "/path/to/thumbnail.jpg",
            },
        )

        path = client.item.thumbnail("KBHG6KA0Y5S9W")
        assert path == "/path/to/thumbnail.jpg"


class TestItemUpdate:
    def test_update(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/v2/item/update",
            json={"status": "success", "data": ITEM_RESPONSE},
        )

        item = client.item.update("KBHG6KA0Y5S9W", tags=["New"], star=5)

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["id"] == "KBHG6KA0Y5S9W"
        assert body["tags"] == ["New"]
        assert body["star"] == 5
        assert isinstance(item.id, str)


class TestItemList:
    def test_list(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=10&orderBy=-CREATEDATE",
            json={"status": "success", "data": [ITEM_RESPONSE]},
        )

        items = client.item.list(limit=10, order_by="-CREATEDATE")
        assert len(items) == 1
        assert items[0].name == "Work"


class TestItemMoveToTrash:
    def test_move_to_trash(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/moveToTrash",
            json={"status": "success"},
        )

        client.item.move_to_trash(["ID1", "ID2"])

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["itemIds"] == ["ID1", "ID2"]


class TestItemRefresh:
    def test_refresh_palette(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/refreshPalette",
            json={"status": "success"},
        )
        client.item.refresh_palette("ID1")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["id"] == "ID1"

    def test_refresh_thumbnail(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/refreshThumbnail",
            json={"status": "success"},
        )
        client.item.refresh_thumbnail("ID1")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["id"] == "ID1"


class TestItemApiError:
    def test_error_response(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/info?id=BAD",
            json={"status": "error"},
        )

        with pytest.raises(EagleApiError):
            client.item.info("BAD")


class TestItemIterAll:
    def _page(self, n: int) -> list[dict]:
        return [{**ITEM_RESPONSE, "id": f"ID{n}_{i}"} for i in range(n)]

    def test_paginates_until_short_page(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        # page_size=2: 満杯ページ2枚 + 端数1件で終端
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=2&offset=0",
            json={"status": "success", "data": self._page(2)},
        )
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=2&offset=1",
            json={"status": "success", "data": self._page(2)},
        )
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=2&offset=2",
            json={"status": "success", "data": self._page(1)},
        )

        items = list(client.item.iter_all(page_size=2))

        assert len(items) == 5
        # offset はページ番号として 0,1,2 と進む
        offsets = [r.url.params["offset"] for r in httpx_mock.get_requests()]
        assert offsets == ["0", "1", "2"]

    def test_stops_immediately_on_empty_first_page(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=200&offset=0",
            json={"status": "success", "data": []},
        )

        assert list(client.item.iter_all()) == []
        assert len(httpx_mock.get_requests()) == 1

    def test_exact_multiple_ends_with_empty_page(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        # 総数がページサイズの倍数 → 追加の空ページで終端を検知
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=2&offset=0",
            json={"status": "success", "data": self._page(2)},
        )
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=2&offset=1",
            json={"status": "success", "data": []},
        )

        assert len(list(client.item.iter_all(page_size=2))) == 2

    def test_filters_are_passed_through(
        self, client: EagleClient, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(json={"status": "success", "data": []})

        list(client.item.iter_all(page_size=10, folders="FOLDER1", ext="png"))

        params = httpx_mock.get_request().url.params
        assert params["folders"] == "FOLDER1"
        assert params["ext"] == "png"
        assert params["limit"] == "10"

    def test_rejects_non_positive_page_size(self, client: EagleClient):
        with pytest.raises(ValueError):
            next(client.item.iter_all(page_size=0))

    def test_is_lazy_iterator(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/list?limit=1&offset=0",
            json={"status": "success", "data": self._page(1) + self._page(0)},
        )

        it = client.item.iter_all(page_size=1)
        # イテレータ生成時点ではリクエストしない
        assert len(httpx_mock.get_requests()) == 0
        next(it)
        assert len(httpx_mock.get_requests()) == 1


class TestItemAddFromUrlsStar:
    def test_star_is_sent_per_item(self, client: EagleClient, httpx_mock: HTTPXMock):
        # #5: AddItemFromUrlParam に star を追加し add_from_url と項目を揃えた
        httpx_mock.add_response(
            url="http://localhost:41595/api/item/addFromURLs",
            json={"status": "success"},
        )
        client.item.add_from_urls(
            [{"url": "https://example.com/a.png", "name": "a", "star": 5}]
        )
        body = json.loads(httpx_mock.get_request().content)
        assert body["items"][0]["star"] == 5
