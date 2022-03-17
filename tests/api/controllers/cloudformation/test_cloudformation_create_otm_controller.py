import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.cloudformation import cloudformation_create_otm_controller
from tests.resources import test_resource_paths

IRIUSRISK_URL = ''

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)

client = TestClient(webapp)


def get_url():
    return cloudformation_create_otm_controller.PREFIX + cloudformation_create_otm_controller.URL


class TestCloudFormationCreateProjectController:

    @pytest.mark.parametrize('project_id,project_name,cft_file',
                             [(None, 'name', open(test_resource_paths.example_json, 'r')),
                              ('id', None, open(test_resource_paths.example_json, 'r')),
                              ('id', 'name', None)])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_file):
        # Given a body
        body = {'id': project_id, 'name': project_name}

        # When I do post on cloudformation endpoint
        files = {'cft_file': cft_file}
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400

    @responses.activate
    def test_create_otm_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == cloudformation_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        assert '"otmVersion": "0.1.0"' in response.text
        assert '"project": ' in response.text
        assert '"name": "project_A_name"' in response.text
        assert '"trustZones":' in response.text
        assert '"components": ' in response.text
