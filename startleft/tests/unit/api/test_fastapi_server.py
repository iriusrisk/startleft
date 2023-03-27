from startleft.startleft.api import fastapi_server


class TestFastapiServer:

    def test_load_custom_openapi_valid(self):
        assert fastapi_server.load_custom_openapi()

