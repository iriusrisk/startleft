import json

import pytest
import responses
from pytest import mark
from pytest import param
from fastapi.testclient import TestClient

from sl_util.sl_util.file_utils import get_byte_data
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources import test_resource_paths

webapp = fastapi_server.webapp
client = TestClient(webapp)
json_mime = 'application/json'

def get_url():
    return diag_create_otm_controller.PREFIX + diag_create_otm_controller.URL

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

octet_stream = 'application/octet-stream'

class TestOTMControllerDiagram:
    @pytest.mark.parametrize('project_id,project_name,diag_file,errors_expected, error_type',
                             [(None, 'name', open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'), 3,
                               'RequestValidationError'),
                              ('id', None, open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'), 3,
                               'RequestValidationError'),
                              ('id', 'name', None, 3, 'RequestValidationError'),
                              ('id', None, None, 4, 'RequestValidationError'),
                              (None, 'name', None, 4, 'RequestValidationError'),
                              ('', None, None, 5, 'RequestValidationError')
                              ])
    def test_create_project_validation_error(self, project_id: str, project_name: str, diag_file, errors_expected: int,
                                             error_type: str):
        # Given a body
        body = {'id': project_id, 'name': project_name}

        # When I do post on diagram endpoint
        files = {'diag_file': diag_file} if diag_file else None
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
    def test_create_project_no_diag_file(self):
        # Given a project_id and name
        project_id: str = 'project_A_id'
        project_name: str = 'project_A_name'

        # And the request files
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on drawio endpoint
        files = {'diag_file': None, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'DRAWIO', 'id': project_id, 'name': project_name}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'

    @responses.activate
    def test_create_project_no_mapping_file(self):
        # Given a project_id and name
        project_id: str = 'project_A_id'
        project_name: str = 'project_A_name'

        # And the request files
        diag_file = get_byte_data(test_resource_paths.drawio_minimal_xml)

        # When I do post on drawio endpoint
        files = {'diag_file': diag_file, 'default_mapping_file': None}
        body = {'diag_type': 'DRAWIO', 'id': project_id, 'name': project_name}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'id': 'project_A_id', 'name': 'project_A_name'},
              "Error in field 'diag_type' located in 'body'. Field required"),
        param({'diag_type': None, 'id': 'project_A_id', 'name': 'project_A_name'},
              "Error in field 'diag_type' located in 'body'. Input should be 'VISIO', 'LUCID', 'DRAWIO' or 'ABACUS'")
    ])
    def test_create_project_no_diag_type(self, body, error_message):
        # Given the request files
        diag_file = get_byte_data(test_resource_paths.drawio_minimal_xml)
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on cloudformation endpoint
        files = {'diag_file': diag_file, 'default_mapping_file': mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                             'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'diag_type': 'DRAWIO', 'name': 'project_A_name'},
              "Error in field 'id' located in 'body'. Field required"),
        param({'diag_type': 'DRAWIO', 'id': None, 'name': 'project_A_name'},
              "Error in field 'id' located in 'body'. String should have at least 1 character")
    ])
    def test_create_project_no_id(self, body, error_message):
        # Given a project_name
        project_name: str = 'project_A_name'

        # Given the request files
        diag_file = get_byte_data(test_resource_paths.drawio_minimal_xml)
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on drawio endpoint
        files = {'diag_file': diag_file, 'default_mapping_file': mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                         'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message

    @responses.activate
    @mark.parametrize('body, error_message', [
        param({'diag_type': 'DRAWIO', 'id': 'project_A_id'},
              "Error in field 'name' located in 'body'. Field required"),
        param({'diag_type': 'DRAWIO', 'id': 'project_A_id', 'name': None},
              "Error in field 'name' located in 'body'. String should have at least 1 character")
        ])
    def test_create_project_no_name(self, body, error_message):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diag_file = get_byte_data(test_resource_paths.drawio_minimal_xml)
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on drawio endpoint
        files = {'diag_file': diag_file, 'default_mapping_file': mapping_file}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert_bad_request_response(response)
        body_response = assert_bad_request_body_response(response, 'RequestValidationError',
                                             'The request is not valid', 'InvalidRequest', 1)
        assert body_response['errors'][0]['errorMessage'] == error_message
