from starlette.testclient import TestClient

from startleft.startleft.api import fastapi_server

webapp = fastapi_server.initialize_webapp()

client = TestClient(webapp)


class TestApiResponse:
    def test_url_not_found(self):
        expected_response = {
            "status": "404",
            "error_type": "HTTPException",
            "title": "Not Found",
            "detail": "http://testserver/wrong/health",
            "errors": []
        }

        response = client.get("/wrong/health")
        assert response.status_code == 404
        assert response.json() == expected_response
