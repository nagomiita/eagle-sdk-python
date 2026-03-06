import json

from pytest_httpx import HTTPXMock

from eagle_sdk import EagleClient


LIBRARY_INFO_RESPONSE = {
    "folders": [{"id": "F1", "name": "Design"}],
    "smartFolders": [{"id": "SF1", "name": "High Res"}],
    "quickAccess": [{"type": "smartFolder", "id": "SF1"}],
    "tagsGroups": [{"id": "TG1", "name": "Style", "tags": ["Modern"], "color": "blue"}],
    "modificationTime": 1592409993367,
    "applicationVersion": "1.11.0",
}


class TestLibraryInfo:
    def test_info(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/library/info",
            json={"status": "success", "data": LIBRARY_INFO_RESPONSE},
        )

        info = client.library.info()

        assert len(info.folders) == 1
        assert len(info.smart_folders) == 1
        assert len(info.quick_access) == 1
        assert len(info.tags_groups) == 1
        assert info.application_version == "1.11.0"


class TestLibraryHistory:
    def test_history(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/library/history",
            json={
                "status": "success",
                "data": ["/path/to/lib1.library", "/path/to/lib2.library"],
            },
        )

        history = client.library.history()
        assert len(history) == 2
        assert history[0] == "/path/to/lib1.library"


class TestLibrarySwitch:
    def test_switch(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/library/switch",
            json={"status": "success"},
        )

        client.library.switch("/path/to/new.library")

        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body["libraryPath"] == "/path/to/new.library"


class TestLibraryIcon:
    def test_icon(self, client: EagleClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="http://localhost:41595/api/library/icon?libraryPath=%2Fpath%2Fto%2Flib.library",
            content=b"\x89PNG\r\n\x1a\n",
        )

        icon_data = client.library.icon("/path/to/lib.library")
        assert icon_data == b"\x89PNG\r\n\x1a\n"
