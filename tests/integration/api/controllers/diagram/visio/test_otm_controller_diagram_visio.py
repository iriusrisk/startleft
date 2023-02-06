import json
from unittest.mock import patch

import responses
from fastapi.testclient import TestClient
from pytest import mark

from slp_base.slp_base.errors import DiagramFileNotValidError, MappingFileNotValidError, LoadingMappingFileError, \
    OtmResultError, OtmBuildingError, LoadingDiagramFileError
from slp_base.tests.util.otm import validate_and_compare_otm, validate_and_compare
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources import test_resource_paths
from tests.resources.test_resource_paths import visio_aws_with_tz_and_vpc, default_visio_mapping, \
    default_visio_mapping_legacy, custom_vpc_mapping, custom_vpc_mapping_legacy, \
    visio_create_otm_ok_only_default_mapping, visio_create_otm_ok_both_mapping_files

IRIUSRISK_URL = ''

webapp = fastapi_server.webapp

client = TestClient(webapp)

VALIDATION_EXCLUDED_REGEX = r"root\[\'dataflows'\]\[.+?\]\['name'\]"


def get_url():
    return diag_create_otm_controller.PREFIX + diag_create_otm_controller.URL


octet_stream = 'application/octet-stream'


class TestOtmControllerDiagramVisio:

    @mark.parametrize('mapping', [default_visio_mapping, default_visio_mapping_legacy])
    @responses.activate
    def test_create_otm_ok_only_default_mapping(self, mapping):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on diagram endpoint
        files = {'diag_file': open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'),
                 'default_mapping_file': open(mapping, 'rb')}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        otm = json.loads(response.text)

        result, expected = validate_and_compare_otm(otm, visio_create_otm_ok_only_default_mapping, VALIDATION_EXCLUDED_REGEX)
        assert result == expected

    @mark.parametrize('default_mapping,custom_mapping', [
        (default_visio_mapping, custom_vpc_mapping),
        (default_visio_mapping_legacy, custom_vpc_mapping_legacy),
        (default_visio_mapping, custom_vpc_mapping_legacy),
        (default_visio_mapping_legacy, custom_vpc_mapping),
    ])
    @responses.activate
    def test_create_otm_ok_both_mapping_files(self, default_mapping, custom_mapping):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on diagram endpoint
        files = {'diag_file': open(visio_aws_with_tz_and_vpc, 'rb'),
                 'default_mapping_file': open(default_mapping, 'rb'),
                 'custom_mapping_file': open(custom_mapping, 'rb')}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        otm = json.loads(response.text)

        result, expected = validate_and_compare(otm, visio_create_otm_ok_both_mapping_files, VALIDATION_EXCLUDED_REGEX)
        assert result == expected

    @responses.activate
    @patch('slp_visio.slp_visio.validate.visio_validator.VisioValidator.validate')
    def test_response_on_validating_diagram_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), octet_stream)
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a DiagramFileNotValidError
        error = DiagramFileNotValidError('Invalid size', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'DiagramFileNotValidError'
        assert body_response['title'] == 'Invalid size'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('slp_visio.slp_visio.parse.visio_parser.VisioParser.build_otm')
    def test_response_on_loading_diagram_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a LoadingDiagramFileError
        error = LoadingDiagramFileError('mocked error title', 'mocked error detail', 'mocked error msg 1')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingDiagramFileError'
        assert body_response['title'] == 'mocked error title'
        assert body_response['detail'] == 'mocked error detail'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'mocked error msg 1'

    @responses.activate
    @patch('slp_visio.slp_visio.validate.visio_mapping_file_validator.VisioMappingFileValidator.validate')
    def test_response_on_validating_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a LoadingDiagramFileError
        error = MappingFileNotValidError('Mapping file does not comply with the schema', 'Schema error',
                                         'schema errors messages')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
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
    @patch('slp_base.slp_base.mapping_file_loader.MappingFileLoader.load')
    def test_response_on_loading_mapping_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a LoadingDiagramFileError
        error = LoadingMappingFileError('Error loading the mapping file. The mapping file ins not valid.',
                                        'AttributeError', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
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
    @patch('slp_base.slp_base.otm_validator.OtmValidator.validate')
    def test_response_on_otm_result_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a LoadingDiagramFileError
        error = OtmResultError('OTM file does not comply with the schema', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
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
    @patch('slp_visio.slp_visio.parse.visio_parser.VisioParser.build_otm')
    def test_response_on_otm_building_error(self, mock_load_source_data):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_file = (default_visio_mapping, open(default_visio_mapping, 'rb'), 'text/yaml')

        # And the mocked method throwing a LoadingDiagramFileError
        error = OtmBuildingError('OTM building error', 'Schema error', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
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

    @mark.parametrize('diagram_source,detail', [
        (b'', 'Provided visio file is not valid. Invalid size'),
        (bytearray(4), 'Provided visio file is not valid. Invalid size'),
        (bytearray(1024 * 1024 * 10 + 1), 'Provided visio file is not valid. Invalid size'),
        (open(default_visio_mapping, 'rb'), 'Invalid content type for diag_file')
    ])
    @responses.activate
    def test_response_on_invalid_diagram_file(self, diagram_source, detail):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the request files
        diagram_source = bytes(diagram_source) if isinstance(diagram_source, bytearray) else diagram_source
        diagram_file = (visio_aws_with_tz_and_vpc, diagram_source, 'application/json')
        mapping_file = ('default_mapping_file', open(default_visio_mapping, 'rb'), 'text/yaml')

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == 'application/json'
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'DiagramFileNotValidError'
        assert body_response['title'] == 'Diagram file is not valid'
        assert body_response['detail'] == detail
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == detail

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
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
        mapping_source = bytes(mapping_source) if isinstance(mapping_source, bytearray) else mapping_source
        mapping_file = ('default_mapping_file', mapping_source, 'text/yaml')

        # When I do post on diagram endpoint
        files = {'diag_file': diagram_file, 'default_mapping_file': mapping_file}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
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
