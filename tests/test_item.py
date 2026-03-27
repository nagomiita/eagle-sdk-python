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
