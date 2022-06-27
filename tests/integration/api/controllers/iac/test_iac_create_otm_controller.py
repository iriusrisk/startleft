import json

import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.iac import iac_create_otm_controller
from startleft.utils.file_utils import FileUtils
from tests.resources.test_resource_paths import default_cloudformation_mapping, default_terraform_mapping, \
    example_json, cloudformation_malformed_mapping_wrong_id, invalid_yaml, \
    terraform_aws_singleton_components_unix_line_breaks

webapp = fastapi_server.initialize_webapp()

client = TestClient(webapp)


def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL


class TestCloudFormationCreateProjectController:

    @pytest.mark.parametrize('project_id,project_name,cft_filename,cft_mimetype,mapping_filename,error_type',
                             [
                                 (None, 'project_A_name', example_json, 'application/json',
                                  default_cloudformation_mapping, 'IacToOtmValidationError'),
                                 ('project_B_id', None, example_json, 'application/json',
                                  default_cloudformation_mapping, 'IacToOtmValidationError'),
                                 ('project_C_id', 'project_C_name', None, None,
                                  default_cloudformation_mapping, 'IacToOtmValidationError'),
                                 ('project_D_id', 'project_D_name', example_json, 'application/json',
                                  None, 'IacToOtmValidationError'),
                                 ('project_E_id', 'project_E_name', example_json, 'application/json',
                                  cloudformation_malformed_mapping_wrong_id, 'MalformedMappingFile'),
                                 ('project_F_id', 'project_F_name', None, None, None, 'IacToOtmValidationError'),
                                 ('project_H_id', 'project_H_name', invalid_yaml, '',
                                  default_cloudformation_mapping, 'IacToOtmValidationError'),
                                 ('project_I_id', 'project_I_name', invalid_yaml, 'text/yaml',
                                  default_cloudformation_mapping, 'IacToOtmValidationError'),
                                 ('project_J_id', 'project_J_name', invalid_yaml, None,
                                  default_cloudformation_mapping, 'IacToOtmValidationError')
                             ])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_filename, cft_mimetype,
                                             mapping_filename, error_type):
        # Given a body
        body = {'iac_type': 'CLOUDFORMATION', 'id': project_id, 'name': project_name}

        # And the request files
        cft_file = None if cft_filename is None else (cft_filename, open(cft_filename, 'r'), cft_mimetype)
        mapping_file = None if mapping_filename is None else (
            mapping_filename, open(mapping_filename, 'rb'), 'text/yaml')
        files = {'iac_file': cft_file, 'mapping_file': mapping_file}

        # When I do post on cloudformation endpoint
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

        # And the request files
        iac_file = (example_json, open(example_json, 'r'), 'application/json')
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'r'), 'text/yaml')

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
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

    @responses.activate
    @pytest.mark.parametrize('filename,break_line', [
        (terraform_aws_singleton_components_unix_line_breaks, '\n'),
        (terraform_aws_singleton_components_unix_line_breaks, '\r\n'),
        (terraform_aws_singleton_components_unix_line_breaks, '\r')
    ])
    def test_create_otm_ok_all_like_breaks(self, filename: str, break_line: str):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (filename, open(filename, 'rb'), 'application/json')
        mapping_file = (default_terraform_mapping, open(default_terraform_mapping, 'r'), 'text/yaml')

        # And the iac_data with custom line breaks
        iac_data = FileUtils.get_byte_data(filename).decode().replace('\n', break_line)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the iac file has the expected line break
        assert f'{break_line} ' in iac_data

        # And the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        assert '"otmVersion": "0.1.0"' in response.text
        assert '"project": ' in response.text
        assert '"name": "project_A_name"' in response.text
        assert '"trustZones": ' in response.text
        assert '"components": ' in response.text
