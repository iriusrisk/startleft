import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.cloudformation import cloudformation_update_project_controller
from startleft.apiclient.base_api_client import IriusRiskApiVersion
from tests.resources import test_resource_paths

IRIUSRISK_URL = 'http://localhost:8080'

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)

client = TestClient(webapp)


def get_url(project_id):
    return cloudformation_update_project_controller.PREFIX + cloudformation_update_project_controller.URL + f"/{project_id}"


class TestCloudFormationUpdateProjectController:

    def test_update_project_api_token_not_set(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'name': 'project_name'}
        response = client.put(get_url(project_id), files=files, data=body)
        assert response.status_code == 401

    @pytest.mark.parametrize('project_id,project_name,cft_file',
                             [('id', 'name', None)])
    def test_update_project_validation_error(self, project_id: str, project_name: str, cft_file):
        # Given a body without project_id
        body = {'name': project_name}

        # When I do put on cloudformation endpoint
        files = {'cft_file': cft_file}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 400

    @responses.activate
    def test_update_existing_project_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And a IriusRisk response mock with the list of existing projects
        responses.add(responses.GET, IRIUSRISK_URL + IriusRiskApiVersion.v1.value + '/products',
                      json=[{'ref': 'project_A_id'}, {'ref': 'project_B_id'}], status=200)

        # And a IriusRisk response mock with the update of the project
        response_body = '{"ref":"project-ref","name":"Project Name"}'
        responses.add(responses.PUT,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f"/products/otm/{project_id}",
                      status=200, body=response_body
                      )

        # When I do put on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'name': 'project_A_name'}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == cloudformation_update_project_controller.RESPONSE_STATUS_CODE
        assert response.text == response_body
        assert len(responses.calls) == 1

    @responses.activate
    def test_update_existing_project_not_found_with_project_name(self):
        # Given a project_id that is always nonexistent
        project_id: str = 'non-existing-id'
        project_name: str = "non-existing-name"

        # And a IriusRisk response mock with the update of the nonexistent project
        responses.add(responses.PUT,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f'/products/otm/{project_id}',
                      status=404)

        # When I do put on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {'name': project_name}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 404
        assert len(responses.calls) == 1

    @responses.activate
    def test_update_existing_project_not_found_no_project_name(self):
        # Given a project_id that is always nonexistent
        project_id: str = 'non-existing-id'

        # And an IriusRisk API get project response mock not found
        responses.add(responses.GET,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f'/products/{project_id}',
                      status=404,
                      json={"status": "error",
                            "errors": [{"message": "Project ID: " + project_id + " not found", "code": "NOT_FOUND"}]})

        # And an IriusRisk API update project response mock ok
        responses.add(responses.PUT,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f'/products/otm/{project_id}',
                      status=204)

        # When I do put on cloudformation endpoint
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 404
        assert responses.calls[0].request.url == 'http://localhost:8080/api/v1/products/' + project_id
        assert len(responses.calls) == 1

    @responses.activate
    def test_update_existing_project_no_project_name(self):
        # Given a project_id that exists
        project_id: str = 'test-id'
        project_name: str = "testId"

        # And an IriusRisk API get project response mock ok
        responses.add(responses.GET,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f'/products/{project_id}',
                      status=200,
                      json={"ref": project_id, "name": project_name})

        # And an IriusRisk API update project response mock ok
        responses.add(responses.PUT,
                      IRIUSRISK_URL + IriusRiskApiVersion.v1.value + f'/products/otm/{project_id}',
                      status=204)

        # When I do a put request on cloudformation endpoint without a name body param
        files = {'cft_file': open(test_resource_paths.example_json, 'r')}
        body = {}
        headers = {'api-token': 'fd865d7d-3e8a-4499-a3e2-937de70bf5c2'}
        response = client.put(get_url(project_id), files=files, data=body, headers=headers)

        # Then
        assert response.status_code == 200
        assert len(responses.calls) == 2
        assert responses.calls[0].request.url == 'http://localhost:8080/api/v1/products/test-id'
        assert responses.calls[1].request.url == 'http://localhost:8080/api/v1/products/otm/test-id'
