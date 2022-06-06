import json

import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.iac import iac_create_otm_controller
from tests.resources import test_resource_paths

webapp = fastapi_server.initialize_webapp()

client = TestClient(webapp)


def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL


class TestCloudFormationCreateProjectController:

    @pytest.mark.parametrize('project_id,project_name,cft_file,mapping_file,error_type',
                             [(None, 'project_A_name', open(test_resource_paths.example_json, 'r'),
                               open(test_resource_paths.default_cloudformation_mapping, 'r'), 'IacToOtmValidationError'),
                              ('project_B_id', None, open(test_resource_paths.example_json, 'r'),
                               open(test_resource_paths.default_cloudformation_mapping, 'r'), 'IacToOtmValidationError'),
                              ('project_C_id', 'project_C_name', None,
                               open(test_resource_paths.default_cloudformation_mapping, 'r'), 'IacToOtmValidationError'),
                              ('project_D_id', 'project_D_name', open(test_resource_paths.example_json, 'r'),
                               None, 'IacToOtmValidationError'),
                              ('project_E_id', 'project_E_name', open(test_resource_paths.example_json, 'r'),
                               open(test_resource_paths.cloudformation_malformed_mapping_wrong_id, 'r'),
                               'MalformedMappingFile'),
                              ('project_F_id', 'project_F_name', None, None, 'IacToOtmValidationError')])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_file, mapping_file,
                                             error_type):
        # Given a body
        body = {'iac_type': 'CLOUDFORMATION', 'id': project_id, 'name': project_name}

        # When I do post on cloudformation endpoint
        files = {'iac_file': cft_file, 'mapping_file': mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        assert response.headers["content-type"] == "application/json"
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type

    @responses.activate
    def test_create_otm_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on cloudformation endpoint
        files = {'iac_file': open(test_resource_paths.example_json, 'r'),
                 'mapping_file': open(test_resource_paths.default_cloudformation_mapping)}
        body = {'iac_type': 'CLOUDFORMATION', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        assert '"otmVersion": "0.1.0"' in response.text
        assert '"project": ' in response.text
        assert '"name": "project_A_name"' in response.text
        assert '"trustZones": ' in response.text
        assert '"components": ' in response.text