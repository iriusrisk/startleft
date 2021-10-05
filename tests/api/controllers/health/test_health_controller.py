import responses
from fastapi.testclient import TestClient

import startleft.api.controllers.health.health_controller
from startleft.api import fastapi_server

IRIUSRISK_URL = 'http://localhost:8080'

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)


client = TestClient(webapp)


class TestHealth:

    @responses.activate
    def test_response(self):
        # Iriusrisk mock response
        responses.add(responses.GET, IRIUSRISK_URL + '/health', status=200)

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == startleft.api.controllers.health.health_controller.RESPONSE_BODY_IRIUSRISK_OK
