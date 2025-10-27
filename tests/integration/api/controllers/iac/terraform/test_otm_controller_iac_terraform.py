import json
from unittest.mock import patch

import pytest
import responses
from fastapi.testclient import TestClient
from pytest import mark

from sl_util.sl_util import file_utils
from slp_base import IacFileNotValidError, LoadingIacFileError, MappingFileNotValidError, \
    LoadingMappingFileError, OTMResultError, OTMBuildingError, IacType
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.iac import iac_create_otm_controller
from tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping, \
    terraform_aws_singleton_components_unix_line_breaks, terraform_malformed_mapping_wrong_id, terraform_gz, \
    invalid_tf, terraform_aws_simple_components, terraform_specific_functions, \
    terraform_mapping_specific_functions, terraform_multiple_files_one, terraform_multiple_files_two

TESTING_IAC_TYPE = IacType.TERRAFORM.value

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'
yaml_mime = 'text/yaml'


def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL


class TestOTMControllerIaCTerraform:
    tf_file = terraform_aws_simple_components
    tf_map = terraform_iriusrisk_tf_aws_mapping
    wrong_id = terraform_malformed_mapping_wrong_id
    uc_a = (None, 'proj A', tf_file, json_mime, tf_map, None, 'RequestValidationError')
    uc_b = ('proj_B', None, tf_file, json_mime, tf_map, None, 'RequestValidationError')
    uc_c = ('proj_C', 'proj C', None, None, tf_map, None, 'RequestValidationError')
    uc_d = ('proj_D', 'proj D', tf_file, json_mime, None, None, 'MappingFileNotValidError')
    uc_e = ('proj_E', 'proj E', tf_file, json_mime, wrong_id, None, 'MappingFileNotValidError')
    uc_f = ('proj_F', 'proj F', None, None, None, None, 'RequestValidationError')
    uc_h = ('proj_H', 'proj H', invalid_tf, '', tf_map, None, 'IacFileNotValidError')
    uc_i = ('proj_I', 'proj I', invalid_tf, yaml_mime, tf_map, None, 'IacFileNotValidError')
    uc_j = ('proj_J', 'proj J', invalid_tf, None, tf_map, None, 'LoadingIacFileError')
    uc_k = ('proj_K', 'proj K', terraform_gz, None, tf_map, None, 'IacFileNotValidError')
    uc_l = ('proj_L', 'proj L', tf_file, json_mime, tf_map, tf_map, 'MappingFileNotValidError')

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
        iac_file = (filename, open(filename, 'rb'), json_mime)
        mapping_file = (terraform_iriusrisk_tf_aws_mapping, open(terraform_iriusrisk_tf_aws_mapping, 'rb'), yaml_mime)

        # And the iac_data with custom line breaks
        iac_data = file_utils.get_byte_data(filename).decode().replace('\n', break_line)

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the iac file has the expected line break
        assert f'{break_line} ' in iac_data

        # And the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == json_mime

        # And the otm is as expected
        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 20
        assert len(otm['dataflows']) == 0

    @mark.parametrize('project_id,project_name,cft_filename,cft_mimetype,mapping_filename,default_mapping_file,error_type',
                      [uc_a, uc_b, uc_c, uc_d, uc_e, uc_f, uc_h, uc_i, uc_j, uc_k, uc_l])
    def test_create_project_validation_error(self, project_id: str, project_name: str, cft_filename, cft_mimetype,
                                             mapping_filename, default_mapping_file, error_type):
        # Given a body
        body = {'iac_type': TESTING_IAC_TYPE, 'id': project_id, 'name': project_name}

        # And the request files
        files = dict()
        if cft_filename:
            files['iac_file'] = (cft_filename, open(cft_filename, 'rb'), cft_mimetype)
        if mapping_filename:
            files['mapping_file'] = (mapping_filename, open(mapping_filename, 'rb'), yaml_mime)
        if default_mapping_file:
            files['default_mapping_file'] = (mapping_filename, open(mapping_filename, 'rb'), 'text/yaml')

        # When I do post on TERRAFORM endpoint
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        assert response.headers['content-type'] == json_mime
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type

    @responses.activate
    @patch('slp_tf.slp_tf.validate.tf_validator.TerraformValidator.validate')
    def test_response_on_validating_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = IacFileNotValidError('Invalid size', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on TERRAFORM endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'IacFileNotValidError'
        assert body_response['title'] == 'Invalid size'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('slp_tf.slp_tf.tf_processor.TerraformProcessor.process')
    def test_response_on_loading_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingIacFileError('mocked error title', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on TERRAFORM endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingIacFileError'
        assert body_response['title'] == 'mocked error title'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('slp_tf.slp_tf.validate.tf_mapping_file_validator.TerraformMappingFileValidator.validate')
    def test_response_on_validating_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = MappingFileNotValidError('Mapping file does not comply with the schema', 'Schema error',
                                         'schema errors messages')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'MappingFileNotValidError'
        assert body_response['title'] == 'Mapping file does not comply with the schema'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'schema errors messages'

    @responses.activate
    @patch('slp_tf.slp_tf.load.tf_mapping_file_loader.TerraformMappingFileLoader.load')
    def test_response_on_loading_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingMappingFileError('Error loading the mapping file. The mapping file ins not valid.',
                                        'AttributeError', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingMappingFileError'
        assert body_response['title'] == 'Error loading the mapping file. The mapping file ins not valid.'
        assert body_response['detail'] == 'AttributeError'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @responses.activate
    @patch('slp_base.slp_base.otm_validator.OTMValidator.validate')
    def test_response_on_otm_result_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = OTMResultError('OTM file does not comply with the schema', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'OTMResultError'
        assert body_response['title'] == 'OTM file does not comply with the schema'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @responses.activate
    @patch('slp_tf.slp_tf.tf_processor.TerraformProcessor.process')
    def test_response_on_otm_building_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_file = (self.tf_map, open(self.tf_map, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = OTMBuildingError('OTM building error', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'OTMBuildingError'
        assert body_response['title'] == 'OTM building error'
        assert body_response['detail'] == 'Schema error'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg'

    @mark.parametrize('iac_source,detail', [
        (b'', 'Provided iac_file is not valid. Invalid size'),
        (bytearray(4), 'Provided iac_file is not valid. Invalid size'),
        (bytearray(1024 * 1024 * 20 + 1), 'Provided iac_file is not valid. Invalid size')])
    @responses.activate
    def test_response_on_invalid_iac_file(self, iac_source, detail):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_source = bytes(iac_source) if isinstance(iac_source, bytearray) else iac_source
        iac_file = (self.tf_file, iac_source, json_mime)
        mapping_file = ('mapping_file', open(self.tf_map, 'rb'), yaml_mime)

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'IacFileNotValidError'
        assert body_response['title'] == 'Terraform file is not valid'
        assert body_response['detail'] == detail
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == detail

    @mark.parametrize('mapping_source,msg', [
        ('small', 'Mapping file does not comply with the schema'),
        (b'', 'Mapping files are not valid. Invalid size'),
        (bytearray(4), 'Mapping files are not valid. Invalid size'),
        (bytearray(1024 * 1024 * 5 + 1), 'Mapping files are not valid. Invalid size')
    ])
    @responses.activate
    def test_response_on_invalid_mapping_file(self, mapping_source, msg):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (self.tf_file, open(self.tf_file, 'rb'), json_mime)
        mapping_source = bytes(mapping_source) if isinstance(mapping_source, bytearray) else mapping_source
        mapping_file = ('mapping_file', mapping_source, yaml_mime)

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'MappingFileNotValidError'
        assert body_response['title'] == 'Mapping files are not valid'
        assert body_response['detail'] == msg
        assert len(body_response['errors']) == 1

    @responses.activate
    def test_mapping_file_terraform_specific_functions(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, containing a mapping file with all terraform specific functions
        iac_file = (terraform_specific_functions, open(terraform_specific_functions, 'rb'), json_mime)
        mapping_file = (
            terraform_mapping_specific_functions, open(terraform_mapping_specific_functions, 'rb'), yaml_mime)

        # When I do post on terraform endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned without errors inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == json_mime

        # And the otm is as expected
        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 3
        assert len(otm['dataflows']) == 0

    @responses.activate
    def test_create_otm_multiple_files_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, two definition files, and one mapping file
        iac_file_one = (
            terraform_multiple_files_one, open(terraform_multiple_files_one, 'rb'),
            json_mime)
        iac_file_two = (
            terraform_multiple_files_two, open(terraform_multiple_files_two, 'rb'),
            json_mime)
        mapping_file = (terraform_iriusrisk_tf_aws_mapping, open(terraform_iriusrisk_tf_aws_mapping, 'rb'), yaml_mime)

        # When I do post on terraform endpoint
        files = [('iac_file', iac_file_one), ('iac_file', iac_file_two), ('mapping_file', mapping_file)]
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == json_mime

        # And the otm is as expected
        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 12
        assert len(otm['dataflows']) == 5

        # And all the expected components are mapped (3 from first, 28 from second)
        assert len(json.loads(response.text)["components"]) == 12

    @responses.activate
    def test_create_otm_multiple_files_on_validating_iac_error(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, two definition files, and one mapping file
        iac_file_valid = (
            terraform_multiple_files_one, open(terraform_multiple_files_one, 'rb'),
            json_mime)
        iac_file_invalid = ''
        mapping_file = (terraform_iriusrisk_tf_aws_mapping, open(terraform_iriusrisk_tf_aws_mapping, 'rb'), yaml_mime)

        files = [('iac_file', iac_file_valid), ('iac_file', iac_file_invalid), ('mapping_file', mapping_file)]
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers['content-type'] == json_mime
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == 'IacFileNotValidError'
