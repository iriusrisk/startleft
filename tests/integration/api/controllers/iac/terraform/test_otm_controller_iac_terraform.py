import json
from unittest.mock import patch

import pytest
import responses
from fastapi.testclient import TestClient
from pytest import mark

from startleft.api import fastapi_server
from startleft.api.controllers.iac import iac_create_otm_controller
from startleft.api.errors import IacFileNotValidError, LoadingIacFileError, MappingFileNotValidError, \
    LoadingMappingFileError, OtmResultError, OtmBuildingError
from startleft.utils.file_utils import FileUtils
from tests.resources.test_resource_paths import default_terraform_mapping, \
    terraform_aws_singleton_components_unix_line_breaks, terraform_malformed_mapping_wrong_id, terraform_gz, \
    visio_aws_shapes, invalid_tf, terraform_aws_simple_components

webapp = fastapi_server.initialize_webapp()

client = TestClient(webapp)


def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL


class TestOtmControllerIaCTerraform:
    tf_file = terraform_aws_simple_components
    tf_map = default_terraform_mapping
    wrong_id = terraform_malformed_mapping_wrong_id
    app_json = 'application/json'
    text_yaml = 'text/yaml'
    uc_a = (None, 'proj A', tf_file, app_json, tf_map, 'RequestValidationError')
    uc_b = ('proj_B', None, tf_file, app_json, tf_map, 'RequestValidationError')
    uc_c = ('proj_C', 'proj C', None, None, tf_map, 'RequestValidationError')
    uc_d = ('proj_D', 'proj D', tf_file, app_json, None, 'RequestValidationError')
    uc_e = ('proj_E', 'proj E', tf_file, app_json, wrong_id, 'MappingFileNotValidError')
    uc_f = ('proj_F', 'proj F', None, None, None, 'RequestValidationError')
    uc_h = ('proj_H', 'proj H', invalid_tf, '', tf_map, 'LoadingIacFileError')
    uc_i = ('proj_I', 'proj I', invalid_tf, text_yaml, tf_map, 'LoadingIacFileError')
    uc_j = ('proj_J', 'proj J', invalid_tf, None, tf_map, 'LoadingIacFileError')
    uc_k = ('proj_K', 'proj K', terraform_gz, None, tf_map, 'IacFileNotValidError')
    uc_l = ('proj_L', 'proj L', visio_aws_shapes, None, tf_map, 'IacFileNotValidError')

    @mark.parametrize('project_id,project_name,cft_filename,cft_mimetype,mapping_filename,error_type',
                      [uc_a, uc_b, uc_c, uc_d, uc_e, uc_f, uc_h, uc_i, uc_j, uc_k])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_filename, cft_mimetype,
                                             mapping_filename, error_type):
        # Given a body
        body = {'iac_type': 'TERRAFORM', 'id': project_id, 'name': project_name}

        # And the request files
        cft_file = None if cft_filename is None else (cft_filename, open(cft_filename, 'rb'), cft_mimetype)
        mapping_file = None if mapping_filename is None else (
            mapping_filename, open(mapping_filename, 'rb'), 'text/yaml')
        files = {'iac_file': cft_file, 'mapping_file': mapping_file}

        # When I do post on TERRAFORM endpoint
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        assert response.headers['content-type'] == 'application/json'
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type

    @responses.activate
    @pytest.mark.parametrize('filename,break_line', [
        (terraform_aws_singleton_components_unix_line_breaks, '\n'),
        (terraform_aws_singleton_components_unix_line_breaks, '\r\n'),
        (terraform_aws_singleton_components_unix_line_breaks, '\r')
    ])
    def test_create_otm_ok_all_line_breaks(self, filename: str, break_line: str):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (filename, open(filename, 'rb'), 'application/json')
        mapping_file = (default_terraform_mapping, open(default_terraform_mapping, 'r'), 'text/yaml')

        # And the iac_data with custom line breaks
        iac_data = FileUtils.get_byte_data(filename).decode().replace('\n', break_line)

        # When I do post on terraform endpoint
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

    @responses.activate
    @patch('startleft.validators.iac_validator.IacValidator.validate')
    def test_response_on_validating_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = IacFileNotValidError('Invalid size', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on TERRAFORM endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'IacFileNotValidError'
        assert body_response['title'] == 'Invalid size'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('startleft.iac.iac_to_otm.IacToOtm.load_source_data')
    def test_response_on_loading_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingIacFileError('mocked error title', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on TERRAFORM endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingIacFileError'
        assert body_response['title'] == 'mocked error title'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('startleft.validators.generic_mapping_validator.GenericMappingValidator.validate')
    def test_response_on_validating_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = MappingFileNotValidError('Mapping file does not comply with the schema', 'Schema error',
                                         'schema errors messages')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'MappingFileNotValidError'
        assert body_response['title'] == 'Mapping file does not comply with the schema'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'schema errors messages'

    @responses.activate
    @patch('startleft.processors.base.mapping_file_loader.MappingFileLoader.load')
    def test_response_on_loading_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingMappingFileError('Error loading the mapping file. The mapping file ins not valid.',
                                        'AttributeError', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingMappingFileError'
        assert body_response['title'] == 'Error loading the mapping file. The mapping file ins not valid.'
        assert body_response['detail'] == 'AttributeError'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @responses.activate
    @patch('startleft.otm.otm_validator.OtmValidator.validate')
    def test_response_on_otm_result_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = OtmResultError('OTM file does not comply with the schema', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'OtmResultError'
        assert body_response['title'] == 'OTM file does not comply with the schema'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @responses.activate
    @patch('startleft.iac.iac_to_otm.IacToOtm.run')
    def test_response_on_otm_building_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'r'), 'application/json')
        mapping_file = (self.tf_map, open(self.tf_map, 'r'), 'text/yaml')

        # And the mocked method throwing a LoadingIacFileError
        error = OtmBuildingError('OTM building error', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'OtmBuildingError'
        assert body_response['title'] == 'OTM building error'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @mark.parametrize('iac_source',
                      [b'', bytearray(4), bytearray(1024 * 1024 * 5 + 1), bytearray(1024 * 5 + 1)])
    @responses.activate
    def test_response_on_invalid_iac_file(self, iac_source):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, self.tf_file, 'application/json')
        mapping_file = ('mapping_file', open(self.tf_map, 'r'), 'text/yaml')

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingIacFileError'
        assert body_response['title'] == 'IaC file is not valid'
        assert len(body_response['errors']) == 1

    @mark.parametrize('mapping_source,msg', [
        (f'small', 'Mapping file does not comply with the schema'),
        (b'', 'Mapping files are not valid. Invalid size'),
        (bytearray(4), 'Mapping files are not valid. Invalid size'),
        (bytearray(1024 * 1024 * 5 + 1), 'Mapping files are not valid. Invalid size')
    ])
    @responses.activate
    def test_response_on_invalid_mapping_file(self, mapping_source, msg):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), 'application/json')
        mapping_file = ('mapping_file', mapping_source, 'text/yaml')

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': 'TERRAFORM', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'MappingFileNotValidError'
        assert body_response['title'] == 'Mapping files are not valid'
        assert body_response['detail'] == msg
        assert len(body_response['errors']) == 1
