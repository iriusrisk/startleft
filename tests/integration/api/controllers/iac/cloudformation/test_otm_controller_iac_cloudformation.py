import json
from unittest.mock import patch

import responses
from fastapi.testclient import TestClient
from pytest import mark

from slp_base import IacType
from slp_base.slp_base.errors import LoadingIacFileError, IacFileNotValidError, MappingFileNotValidError, \
    LoadingMappingFileError, OTMResultError, OTMBuildingError
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.iac import iac_create_otm_controller
from tests.resources.test_resource_paths import default_cloudformation_mapping, example_json, \
    cloudformation_malformed_mapping_wrong_id, invalid_yaml, cloudformation_all_functions, \
    cloudformation_mapping_all_functions, cloudformation_gz, visio_aws_shapes, cloudformation_multiple_files_networks, \
    cloudformation_multiple_files_resources, cloudformation_ref_full_syntax, cloudformation_ref_short_syntax

TESTING_IAC_TYPE = IacType.CLOUDFORMATION.value

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'


def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL


yaml_mime = 'text/yaml'


class TestOTMControllerIaCCloudformation:
    cft_map = default_cloudformation_mapping
    wrong_id = cloudformation_malformed_mapping_wrong_id
    uc_a = (None, 'proj A', example_json, json_mime, cft_map, 'RequestValidationError')
    uc_b = ('proj_B', None, example_json, json_mime, cft_map, 'RequestValidationError')
    uc_c = ('proj_C', 'proj C', None, None, cft_map, 'RequestValidationError')
    uc_d = ('proj_D', 'proj D', example_json, json_mime, None, 'RequestValidationError')
    uc_e = ('proj_E', 'proj E', example_json, json_mime, wrong_id, 'MappingFileNotValidError')
    uc_f = ('proj_F', 'proj F', None, None, None, 'RequestValidationError')
    uc_h = ('proj_H', 'proj H', invalid_yaml, '', cft_map, 'IacFileNotValidError')
    uc_i = ('proj_I', 'proj I', invalid_yaml, yaml_mime, cft_map, 'OTMBuildingError')
    uc_j = ('proj_J', 'proj J', invalid_yaml, None, cft_map, 'OTMBuildingError')
    uc_k = ('proj_K', 'proj K', cloudformation_gz, None, cft_map, 'IacFileNotValidError')
    uc_l = ('proj_L', 'proj L', visio_aws_shapes, None, cft_map, 'IacFileNotValidError')

    @responses.activate
    def test_create_otm_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
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
        assert len(otm['components']) == 5
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

        # When I do post on cloudformation endpoint
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers['content-type'] == json_mime
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type

    @responses.activate
    @patch('slp_cft.slp_cft.validate.cft_validator.CloudformationValidator.validate')
    def test_response_on_validating_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = IacFileNotValidError('Invalid size', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
    @patch('slp_cft.slp_cft.load.cft_loader.CloudformationLoader.load')
    def test_response_on_loading_iac_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingIacFileError('mocked error title', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
    @patch('slp_cft.slp_cft.load.cft_mapping_file_loader.CloudformationMappingFileLoader.load')
    def test_response_on_validating_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = MappingFileNotValidError('Mapping file does not comply with the schema', 'Schema error',
                                         'schema errors messages')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
    @patch('slp_cft.slp_cft.load.cft_mapping_file_loader.CloudformationMappingFileLoader.load')
    def test_response_on_loading_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = LoadingMappingFileError('Error loading the mapping file. The mapping file ins not valid.',
                                        'AttributeError', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = OTMResultError('OTM file does not comply with the schema', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
    @patch('slp_cft.slp_cft.cft_processor.CloudformationProcessor.process')
    def test_response_on_otm_building_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # And the mocked method throwing a LoadingIacFileError
        error = OTMBuildingError('OTM building error', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on cloudformation endpoint
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
        (bytearray(1024 * 1024 * 20 + 1), 'Provided iac_file is not valid. Invalid size')
    ])
    @responses.activate
    def test_response_on_invalid_iac_file(self, iac_source, detail):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_source = bytes(iac_source) if isinstance(iac_source, bytearray) else iac_source
        iac_file = (example_json, iac_source, json_mime)
        mapping_file = ('mapping_file', open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'IacFileNotValidError'
        assert body_response['title'] == 'CloudFormation file is not valid'
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
        iac_file = (example_json, example_json, json_mime)
        mapping_source = bytes(mapping_source) if isinstance(mapping_source, bytearray) else mapping_source
        mapping_file = ('mapping_file', mapping_source, yaml_mime)

        # When I do post on cloudformation endpoint
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
    def test_mapping_file_cloudformation_all_functions(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, containing a mapping file with all cloudformation functions
        iac_file = (cloudformation_all_functions, open(cloudformation_all_functions, 'rb'), json_mime)
        mapping_file = (
            cloudformation_mapping_all_functions, open(cloudformation_mapping_all_functions, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # And the otm is as expected
        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 5
        assert len(otm['dataflows']) == 0

        # And all the expected components are mapped
        assert len(json.loads(response.text)["components"]) == 5

    @responses.activate
    def test_create_otm_multiple_files_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, two definition files, and one mapping file
        iac_file_networks = (
            cloudformation_multiple_files_networks, open(cloudformation_multiple_files_networks, 'rb'),
            json_mime)
        iac_file_resources = (
            cloudformation_multiple_files_resources, open(cloudformation_multiple_files_resources, 'rb'),
            json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = [('iac_file', iac_file_networks), ('iac_file', iac_file_resources), ('mapping_file', mapping_file)]
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
        assert len(otm['trustZones']) == 2
        assert len(otm['components']) == 22
        assert len(otm['dataflows']) == 22

    @responses.activate
    def test_create_otm_multiple_files_on_validating_iac_error(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files, two definition files, and one mapping file
        iac_file_valid = (
            cloudformation_multiple_files_networks, open(cloudformation_multiple_files_networks, 'rb'),
            json_mime)
        iac_file_invalid = ''
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = [('iac_file', iac_file_valid), ('iac_file', iac_file_invalid), ('mapping_file', mapping_file)]
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers['content-type'] == json_mime
        res_body = json.loads(response.content.decode('utf-8'))
        assert res_body['status'] == '400'
        assert res_body['error_type'] == 'IacFileNotValidError'

    @mark.parametrize('filename', [cloudformation_ref_full_syntax, cloudformation_ref_short_syntax])
    @responses.activate
    def test_yaml_ref_function_is_parsed(self, filename):
        # Given a project_id and project_name
        project_id: str = 'project_A_id'
        project_name: str = 'project_A_name'

        # And the request files
        iac_file = (filename, open(filename, 'rb'), yaml_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': project_name}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        otm = json.loads(response.text)
        assert otm["components"][0]["name"] == "0.0.0.0/0"
