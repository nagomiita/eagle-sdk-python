import json

from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient

FOLDER_RESPONSE = {
    "id": "KBJJSMMVF9WYL",
    "name": "Test Folder",
    "images": [],
    "folders": [],
    "modificationTime": 1592409993367,
    "imagesMappings": {},
    "tags": [],
    "children": [],
    "isExpand": True,
}

FOLDER_LIST_RESPONSE = {
    "id": "KBJJSMMVF9WYL",
    "name": "Design",
    "description": "Design assets",
    "children": [],
    "modificationTime": 1592409993367,
    "tags": ["ui"],
    "imageCount": 30,
    "descendantImageCount": 45,
    "pinyin": "Design",
    "extendTags": [],
}


class TestFolderCreate:
    def test_create(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/create",
            json={"status": "success", "data": FOLDER_RESPONSE},
        )

        folder = client.folder.create("Test Folder")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["folderName"] == "Test Folder"
        assert folder.id == "KBJJSMMVF9WYL"
        assert folder.name == "Test Folder"

    def test_create_with_parent(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/create",
            json={"status": "success", "data": FOLDER_RESPONSE},
        )

        client.folder.create("Test Folder", parent="PARENT_ID")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["parent"] == "PARENT_ID"


class TestFolderRename:
    def test_rename(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/rename",
            json={"status": "success", "data": FOLDER_RESPONSE},
        )

        folder = client.folder.rename("KBJJSMMVF9WYL", "New Name")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["folderId"] == "KBJJSMMVF9WYL"
        assert body["newName"] == "New Name"
        assert isinstance(folder.id, str)


class TestFolderUpdate:
    def test_update(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/update",
            json={"status": "success", "data": FOLDER_RESPONSE},
        )

        client.folder.update(
            "KBJJSMMVF9WYL",
            new_name="Updated",
            new_description="Desc",
            new_color="red",
        )

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["folderId"] == "KBJJSMMVF9WYL"
        assert body["newName"] == "Updated"
        assert body["newDescription"] == "Desc"
        assert body["newColor"] == "red"


class TestFolderList:
    def test_list(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/list",
            json={"status": "success", "data": [FOLDER_LIST_RESPONSE]},
        )

        folders = client.folder.list()
        assert len(folders) == 1
        assert folders[0].name == "Design"
        assert folders[0].image_count == 30
        assert folders[0].descendant_image_count == 45


class TestFolderListRecent:
    def test_list_recent(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/folder/listRecent",
            json={"status": "success", "data": [FOLDER_LIST_RESPONSE]},
        )

        folders = client.folder.list_recent()
        assert len(folders) == 1
