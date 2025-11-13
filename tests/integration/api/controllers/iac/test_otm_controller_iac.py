import json

import responses
from pytest import mark
from pytest import param
from fastapi.testclient import TestClient
from slp_base import IacType

from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.iac import iac_create_otm_controller

from tests.resources.test_resource_paths import (default_cloudformation_mapping, example_json, \
     cloudformation_empty_file, cloudformation_for_security_group_tests_json, old_cloudformation_default_mapping, \
     cloudformation_custom_mapping_file, cloudformation_wrong_mapping_file)

DEFAULT_TESTING_IAC_TYPE = IacType.CLOUDFORMATION.value
IAC_FILE_FOR_MAPPING_VALIDATIONS = cloudformation_for_security_group_tests_json
DEFAULT_MAPPING_FILE = old_cloudformation_default_mapping
MAPPING_FILE = default_cloudformation_mapping
CUSTOM_MAPPING_FILE = cloudformation_custom_mapping_file
INVALID_MAPPING_FILE = cloudformation_wrong_mapping_file

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'
yaml_mime = 'text/yaml'

def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL

def assert_bad_request_response(response):
    assert response.status_code == 400
    assert response.headers.get('content-type') == json_mime

def assert_bad_request_body_response(response, error_type, title, detail, total_errors):
    body_response = json.loads(response.text)
    assert body_response['status'] == '400'
    assert body_response['error_type'] == error_type
    assert body_response['title'] == title
    assert body_response['detail'] == detail
    assert len(body_response['errors']) == total_errors
    return body_response

def get_iac_file_for_mapping_validations():
    return IAC_FILE_FOR_MAPPING_VALIDATIONS, open(IAC_FILE_FOR_MAPPING_VALIDATIONS, 'rb'), json_mime

def get_mapping_file_for_mapping_validations(mapping_file_path):
    return mapping_file_path, open(mapping_file_path, 'rb'), yaml_mime

class TestOTMControllerIaC:
    @responses.activate
    def test_controller_no_iac_file(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': None, 'mapping_file': mapping_file}
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'

    @responses.activate
    def test_controller_empty_iac_file(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (cloudformation_empty_file, open(cloudformation_empty_file, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'IacFileNotValidError',
         'CloudFormation file is not valid', 'Provided iac_file is not valid. Invalid size', 1)
        assert (body_response['errors'][0]['errorMessage'] == "Provided iac_file is not valid. Invalid size")

    @responses.activate
    def test_controller_no_mapping_file(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': None}
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'id': 'project_A_id', 'name': 'project_A_name'},
          "Error in field 'iac_type' located in 'body'. Field required"),
        param({'iac_type': None, 'id': 'project_A_id', 'name': 'project_A_name'},
          "Error in field 'iac_type' located in 'body'. Input should be 'CLOUDFORMATION', 'TERRAFORM' or 'TFPLAN'")
    ])
    def test_controller_no_iac_type(self, body, error_message):
        # Given the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                 'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    def test_controller_no_id(self):
        # Given the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': None, 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                         'The request is not valid', 'InvalidRequest', 1)
        assert (body_response['errors'][0]['errorMessage'] ==
            "Error in field 'id' located in 'body'. String should have at least 1 character")

    @responses.activate
    def test_controller_no_name(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        iac_file = (example_json, open(example_json, 'rb'), json_mime)
        mapping_file = (default_cloudformation_mapping, open(default_cloudformation_mapping, 'rb'), yaml_mime)

        # When I do post on cloudformation endpoint
        files = {'iac_file': iac_file, 'mapping_file': mapping_file}
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': None}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                         'The request is not valid', 'InvalidRequest', 1)
        assert (body_response['errors'][0]['errorMessage'] ==
            "Error in field 'name' located in 'body'. String should have at least 1 character")

    @responses.activate
    @mark.parametrize('expected_mapped_components, files', [
        param(22,
              {
                  'iac_file': get_iac_file_for_mapping_validations(),
                  'default_mapping_file': get_mapping_file_for_mapping_validations(DEFAULT_MAPPING_FILE)},
              id="case A: (201) default_mapping_file"),
        param(22,
              {
                  'iac_file': get_iac_file_for_mapping_validations(),
                  'mapping_file': get_mapping_file_for_mapping_validations(MAPPING_FILE)},
              id="case B: (201) mapping_file"),
        param(28,
              {
                  'iac_file': get_iac_file_for_mapping_validations(),
                  'default_mapping_file': get_mapping_file_for_mapping_validations(DEFAULT_MAPPING_FILE),
                  'custom_mapping_file': get_mapping_file_for_mapping_validations(CUSTOM_MAPPING_FILE)},
              id="case C: (201) default_mapping_file + custom_mapping_file"),
        param(28,
              {
                  'iac_file': get_iac_file_for_mapping_validations(),
                  'mapping_file': get_mapping_file_for_mapping_validations(MAPPING_FILE),
                  'custom_mapping_file': get_mapping_file_for_mapping_validations(CUSTOM_MAPPING_FILE)},
              id="case D: (201) mapping_file + custom_mapping_file")
    ])
    def test_mapping_files_validations_success(self, expected_mapped_components, files):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on cloudformation endpoint
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == json_mime

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 2
        assert len(otm['components']) == expected_mapped_components
        assert len(otm['dataflows']) == 22

    @responses.activate
    @mark.parametrize('files, title, detail, error_message', [
        param({
                'iac_file': get_iac_file_for_mapping_validations(),
                'default_mapping_file': get_mapping_file_for_mapping_validations(DEFAULT_MAPPING_FILE),
                'mapping_file': get_mapping_file_for_mapping_validations(MAPPING_FILE)},
            "Error processing mapping file",
            "default_mapping_file and mapping_file cannot be present at the same time",
            "default_mapping_file and mapping_file cannot be present at the same time",
            id="case E: (400) default_mapping_file + mapping_file"),
        param({
                'iac_file': get_iac_file_for_mapping_validations(),
                'default_mapping_file': get_mapping_file_for_mapping_validations(DEFAULT_MAPPING_FILE),
                'mapping_file': get_mapping_file_for_mapping_validations(MAPPING_FILE),
                'custom_mapping_file': get_mapping_file_for_mapping_validations(CUSTOM_MAPPING_FILE)},
            "Error processing mapping file",
            "default_mapping_file and mapping_file cannot be present at the same time",
            "default_mapping_file and mapping_file cannot be present at the same time",
            id="case F: (400) default_mapping_file + mapping_file + custom_mapping_file"),
        param({
                'iac_file': get_iac_file_for_mapping_validations(),
                'default_mapping_file': get_mapping_file_for_mapping_validations(INVALID_MAPPING_FILE)},
            "Error reading the mapping file. The mapping files are not valid.",
            "ParserError",
            'while parsing a flow node\nexpected the node content, but found \'<stream end>\'\n  in \"<byte string>\", line 2, column 1:\n    \n    ^',
            id="case G: (400) default_mapping_file (WRONG mapping file)"),
        param({
                'iac_file': get_iac_file_for_mapping_validations(),
                'mapping_file': get_mapping_file_for_mapping_validations(INVALID_MAPPING_FILE)},
            "Error reading the mapping file. The mapping files are not valid.",
            "ParserError",
            'while parsing a flow node\nexpected the node content, but found \'<stream end>\'\n  in \"<byte string>\", line 2, column 1:\n    \n    ^',
            id="case H: (400) mapping_file (WRONG mapping file)"),
        param({
                'iac_file': get_iac_file_for_mapping_validations(),
                'custom_mapping_file': get_mapping_file_for_mapping_validations(INVALID_MAPPING_FILE)},
            "Error processing mapping file",
            "Mapping file must not be void",
            "Mapping file must not be void",
            id="case I: (400) custom_mapping_file (WRONG mapping file)")
    ])
    def test_mapping_files_validations_errors(self, files, title, detail, error_message):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on cloudformation endpoint
        body = {'iac_type': DEFAULT_TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response,
         'MappingFileNotValidError', title, detail, 1)
        assert body_response['errors'][0]['errorMessage'] == error_message
