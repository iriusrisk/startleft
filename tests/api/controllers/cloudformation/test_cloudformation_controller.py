import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.cloudformation import cloudformation_controller
from startleft.iriusrisk import IriusRisk
from tests.resources import test_resource_paths

IRIUSRISK_URL = 'http://localhost:8080'

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)

client = TestClient(webapp)


def get_url_post():
    return cloudformation_controller.PREFIX + cloudformation_controller.URL


def get_url_put(project_id):
    return cloudformation_controller.PREFIX + cloudformation_controller.URL + f"/projects/{project_id}"


class TestCloudFormationController:

    def test_create_project_api_token_not_set(self):
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'id': 'project_id', 'name': 'project_name', 'type': 'JSON'}
        response = client.post(get_url_post(), files=files, data=body)
        assert response.status_code == 401

    @pytest.mark.parametrize('project_id,project_name,project_type,cft_file',
                             [(None, 'name', 'type', open(test_resource_paths.example_json, 'r')),
                              ('id', None, 'type', open(test_resource_paths.example_json, 'r')),
                              ('id', 'name', None, open(test_resource_paths.example_json, 'r')),
                              ('id', 'name', 'type', None)])
    def test_create_project_validation_error(self, project_id: str, project_name: str, project_type: str, cft_file):
        # Given a body
        body = {'id': project_id, 'name': project_name, 'type': project_type}

        # When I do post on cloudformation endpoint
        files = {'cft_file': cft_file}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.post(get_url_post(), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 400

    @responses.activate
    def test_create_not_existing_project_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And a IriusRisk response mock with the list of existing projects
        responses.add(responses.GET, IRIUSRISK_URL + IriusRisk.API_PATH + '/products',
                      json=[{'ref': 'project_B_id'}, {'ref': 'project_C_id'}], status=200)

        # And a IriusRisk response mock with the creation of the project
        responses.add(responses.POST, IRIUSRISK_URL + IriusRisk.API_PATH + '/products/upload/',
                      status=200)

        # And a response mock with the execution of the rules
        responses.add(responses.PUT, IRIUSRISK_URL + IriusRisk.API_PATH + f"/rules/product/{project_id}")

        # When I do post on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'id': f'{project_id}', 'name': 'project_A_name', 'type': 'JSON'}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.post(get_url_post(), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == cloudformation_controller.RESPONSE_STATUS_CODE_POST
        assert response.json() == cloudformation_controller.RESPONSE_BODY

    def test_update_project_api_token_not_set(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'name': 'project_name', 'type': 'JSON'}
        response = client.put(get_url_put(project_id), files=files, data=body)
        assert response.status_code == 401

    @pytest.mark.parametrize('project_id,project_type,cft_file',
                             [(None, 'type', open(test_resource_paths.example_json, 'r')),
                              ('id', 'type', open(test_resource_paths.example_json, 'r')),
                              ('id', None, open(test_resource_paths.example_json, 'r')),
                              ('id', 'type', None)])
    def test_update_project_validation_error(self, project_id: str, project_type: str, cft_file):
        # Given a body
        body = {'type': project_type}

        # When I do post on cloudformation endpoint
        files = {'cft_file': cft_file}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url_put(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 400

    @responses.activate
    def test_update_not_existing_project_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And a IriusRisk response mock with the list of existing projects
        responses.add(responses.GET, IRIUSRISK_URL + IriusRisk.API_PATH + '/products',
                      json=[{'ref': 'project_B_id'}, {'ref': 'project_C_id'}], status=200)

        # And a IriusRisk response mock with the creation of the project
        responses.add(responses.POST, IRIUSRISK_URL + IriusRisk.API_PATH + '/products/upload/',
                      status=200)

        # And a response mock with the execution of the rules
        responses.add(responses.PUT, IRIUSRISK_URL + IriusRisk.API_PATH + f"/rules/product/{project_id}")

        # When I do post on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'name': 'project_A_name', 'type': 'JSON'}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url_put(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == cloudformation_controller.RESPONSE_STATUS_CODE_PUT
        assert response.json() == cloudformation_controller.RESPONSE_BODY
