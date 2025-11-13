import json
from http import HTTPStatus

import pytest
import responses
from pytest import mark, param
from fastapi.testclient import TestClient
from slp_base.slp_base.provider_type import application_octet_stream, application_json, VALID_YAML_MIME_TYPES as application_yaml

from slp_base import EtmType

from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.etm import etm_create_otm_controller
from startleft.tests.resources.test_resource_paths import mtmt_invalid_file as mtmt_invalid_zip_file
from tests.resources.test_resource_paths import mtmt_valid_file, mtmt_mapping_mvp, mtmt_mapping_file_custom, \
    empty_mapping_file, mtmt_invalid_file

TESTING_ETM_TYPE = EtmType.MTMT.value
PROJECT_ID = 'project_A_id'
PROJECT_NAME = 'project_A_name'

webapp = fastapi_server.webapp
client = TestClient(webapp)

def get_url():
    return etm_create_otm_controller.PREFIX + etm_create_otm_controller.URL

def get_file(file_path, mime_type):
    return file_path, open(file_path, 'rb'), mime_type

def assert_bad_request_response(response):
    assert response.status_code == 400
    assert response.headers.get('content-type') == application_json

def assert_bad_request_body_response(response, error_type, title, detail, total_errors):
    body_response = json.loads(response.text)
    assert body_response['status'] == '400'
    assert body_response['error_type'] == error_type
    assert body_response['title'] == title
    assert body_response['detail'] == detail
    assert len(body_response['errors']) == total_errors
    return body_response

class TestOTMControllerEtm:

    @pytest.mark.parametrize("project_id,project_name,source_file,errors_expected, error_type", [
        (None, 'name', None, 4, 'RequestValidationError'),
        ('id', None, None, 4, 'RequestValidationError'),
        ('id', 'name', None, 3, 'RequestValidationError'),
        (None, None, None, 5, 'RequestValidationError'),
        ('', None, None, 5, 'RequestValidationError')
    ])
    def test_create_project_validation_error(self, project_id: str, project_name: str,
                                             source_file, errors_expected: int, error_type: str):
        # Given a body
        body = {'id': project_id, 'name': project_name}

        # When I do post to the endpoint
        files = {'source_file': source_file} if source_file else None
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        res_body = json.loads(response.text)
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type
        assert len(res_body['errors']) == errors_expected
        for e in res_body['errors']:
            assert len(e['errorMessage']) > 0

    @responses.activate
    @mark.parametrize("custom_mapping_file_path,expected_component_type",
          [param(mtmt_mapping_mvp, "web-service", id="default_as_custom"),
           param(mtmt_mapping_file_custom, "empty-component", id="custom_overrides_default"),
           param(None, "web-service", id="no_custom_mapping")])
    def test_custom_mapping_file(self, custom_mapping_file_path, expected_component_type):
        # Given a body
        body = {'id': PROJECT_ID, 'name': PROJECT_NAME, 'source_type': TESTING_ETM_TYPE}

        # When I do post to the endpoint
        source_file = get_file(mtmt_valid_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])
        files = [('source_file', source_file), ('default_mapping_file', default_mapping_file)]
        if custom_mapping_file_path:
            custom_mapping_file = get_file(custom_mapping_file_path, application_yaml[1])
            files.append(('custom_mapping_file', custom_mapping_file))
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert HTTPStatus.CREATED == response.status_code
        assert application_json == response.headers.get('content-type')

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == PROJECT_ID
        assert otm['project']['name'] == PROJECT_NAME
        assert otm['project']['name'] == PROJECT_NAME
        assert len(otm['trustZones']) == 2
        assert len(otm['components']) == 4
        assert len(otm['dataflows']) == 6
        assert otm['components'][2]['type'] == expected_component_type

    @responses.activate
    def test_create_project_no_source_file(self):
        # Given the request files
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'default_mapping_file': default_mapping_file}
        body = {'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                     'The request is not valid', 'InvalidRequest', 1)
        assert (body_response['errors'][0]['errorMessage'] ==
                "Error in field 'source_file' located in 'body'. Field required")

    @responses.activate
    def test_create_project_no_mapping_file(self):
        # Given the request files
        source_file = get_file(mtmt_valid_file, application_octet_stream)

        # When I do post on drawio endpoint
        files = {'source_file': source_file}
        body = {'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                 'The request is not valid', 'InvalidRequest', 1)
        assert (body_response['errors'][0]['errorMessage'] ==
                "Error in field 'default_mapping_file' located in 'body'. Field required")

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'id': PROJECT_ID, 'name': PROJECT_NAME},
              "Error in field 'source_type' located in 'body'. Field required"),
        param({'source_type': None, 'id': PROJECT_ID, 'name': PROJECT_NAME},
              "Error in field 'source_type' located in 'body'. Input should be 'MTMT'") ])
    def test_create_project_no_source_type(self, body, error_message):
        # Given the request files
        source_file = get_file(mtmt_valid_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                     'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'source_type': TESTING_ETM_TYPE, 'name': PROJECT_NAME},
              "Error in field 'id' located in 'body'. Field required"),
        param({'source_type': TESTING_ETM_TYPE, 'id': None, 'name': PROJECT_NAME},
              "Error in field 'id' located in 'body'. String should have at least 1 character") ])
    def test_create_project_no_id(self, body, error_message):
        # Given the request files
        source_file = get_file(mtmt_valid_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                     'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID},
              "Error in field 'name' located in 'body'. Field required"),
        param({'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': None},
              "Error in field 'name' located in 'body'. String should have at least 1 character") ])
    def test_create_project_no_name(self, body, error_message):
        # Given the request files
        source_file = get_file(mtmt_valid_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                     'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    def test_create_project_invalid_empty_mapping_file(self):
        # Given the request files
        source_file = get_file(mtmt_valid_file, application_octet_stream)
        default_mapping_file = get_file(empty_mapping_file, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        body = {'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'MappingFileNotValidError',
                 'Mapping files are not valid', 'Mapping files are not valid. Invalid size', 1)
        assert (body_response['errors'][0]['errorMessage'] == "Mapping files are not valid. Invalid size")

    @responses.activate
    def test_create_project_invalid_zip_source_file(self):
        # Given the request files
        source_file = get_file(mtmt_invalid_zip_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        body = {'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'SourceFileNotValidError',
     'Microsoft Threat Modeling Tool file is not valid', 'Invalid content type for source_file', 1)
        assert (body_response['errors'][0]['errorMessage'] == "Invalid content type for source_file")

    @responses.activate
    def test_create_project_invalid_format_source_file(self):
        # Given the request files
        source_file = get_file(mtmt_invalid_file, application_octet_stream)
        default_mapping_file = get_file(mtmt_mapping_mvp, application_yaml[1])

        # When I do post on drawio endpoint
        files = {'source_file': source_file, 'default_mapping_file': default_mapping_file}
        body = {'source_type': TESTING_ETM_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'LoadingSourceFileError',
                                     'Source file cannot be loaded', 'ParseError', 1)
        assert (body_response['errors'][0]['errorMessage'] == "syntax error: line 1, column 0")
