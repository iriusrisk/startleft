from fastapi.testclient import TestClient

import startleft.api.controllers.health.health_controller
from startleft.api import fastapi_server

webapp = fastapi_server.initialize_webapp('http://localhost:8080')

client = TestClient(webapp)


class TestHealth:

    def test_response(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == startleft.api.controllers.health.health_controller.RESPONSE_BODY
