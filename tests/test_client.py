from eagle_sdk import EagleClient
from eagle_sdk.api.application import ApplicationAPI
from eagle_sdk.api.folder import FolderAPI
from eagle_sdk.api.item import ItemAPI
from eagle_sdk.api.library import LibraryAPI


class TestEagleClient:
    def test_default_base_url(self):
        client = EagleClient()
        assert client._http._client.base_url == "http://localhost:41595"

    def test_custom_base_url(self):
        client = EagleClient(base_url="http://localhost:9999")
        assert client._http._client.base_url == "http://localhost:9999"

    def test_properties(self):
        client = EagleClient()
        assert isinstance(client.application, ApplicationAPI)
        assert isinstance(client.item, ItemAPI)
        assert isinstance(client.folder, FolderAPI)
        assert isinstance(client.library, LibraryAPI)

    def test_context_manager(self):
        with EagleClient() as client:
            assert isinstance(client, EagleClient)
