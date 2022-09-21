import responses
from fastapi.testclient import TestClient

import startleft.startleft.api.controllers.health.health_controller
from startleft.startleft.api import fastapi_server

webapp = fastapi_server.initialize_webapp()


client = TestClient(webapp)


class TestHealth:

    @responses.activate
    def test_response(self):

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == startleft.startleft.api.controllers.health.health_controller.RESPONSE_BODY_STARTLEFT_OK
