import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.cloudformation import cloudformation_create_project_controller
from startleft.apiclient.base_api_client import IriusRiskApiVersion
from tests.resources import test_resource_paths

IRIUSRISK_URL = 'http://localhost:8080'

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)

client = TestClient(webapp)


def get_url():
    return cloudformation_create_project_controller.PREFIX + cloudformation_create_project_controller.URL


class TestCloudFormationCreateProjectController:

    def test_create_project_api_token_not_set(self):
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'id': 'project_id', 'name': 'project_name'}
        response = client.post(get_url(), files=files, data=body)
        assert response.status_code == 401

    @pytest.mark.parametrize('project_id,project_name,cft_file',
                             [(None, 'name', open(test_resource_paths.example_json, 'r')),
                              ('id', None, open(test_resource_paths.example_json, 'r')),
                              ('id', 'name', None)])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_file):
        # Given a body
        body = {'id': project_id, 'name': project_name}

        # When I do post on cloudformation endpoint
        files = {'cft_file': cft_file}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.post(get_url(), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 400

    @responses.activate
    def test_create_not_existing_project_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And a IriusRisk response mock with the list of existing projects
        responses.add(responses.GET, IRIUSRISK_URL + IriusRiskApiVersion.v1.value + '/products',
                      json=[{'ref': 'project_B_id'}, {'ref': 'project_C_id'}], status=200)

        # And a IriusRisk response mock with the creation of the project
        responses.add(responses.POST, IRIUSRISK_URL + IriusRiskApiVersion.v1.value + '/products/otm',
                      status=200)

        # When I do post on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'id': f'{project_id}', 'name': 'project_A_name'}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.post(get_url(), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == cloudformation_create_project_controller.RESPONSE_STATUS_CODE
        assert response.json() == cloudformation_create_project_controller.RESPONSE_BODY
