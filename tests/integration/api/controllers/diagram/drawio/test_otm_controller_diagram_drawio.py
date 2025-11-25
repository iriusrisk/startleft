import json

import pytest
import responses
from fastapi.testclient import TestClient
from slp_base.slp_base.provider_type import application_json
from tests.integration.api.controllers.diagram.test_otm_controller_diagram import get_url

from tests.resources import test_resource_paths

from sl_util.sl_util.file_utils import get_byte_data
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources.test_resource_paths import default_drawio_mapping, custom_drawio_mapping, drawio_minimal_xml, \
    terraform_aws_simple_components, invalid_extension_mtmt_file

webapp = fastapi_server.webapp
client = TestClient(webapp)

class TestOTMControllerDiagramDrawio:

    @responses.activate
    def test_create_otm_multi_page_error(self):
        # Given a project_id
        project_id: str = 'test_multi_page_error'

        # And the multi-page source file
        diag_file = get_byte_data(test_resource_paths.drawio_multi_page)

        # And the mapping file
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on diagram endpoint
        files = {'diag_file': (test_resource_paths.drawio_multi_page, diag_file),
                 'default_mapping_file': mapping_file}
        body = {'diag_type': 'DRAWIO', 'id': project_id, 'name': project_id}
        response = client.post(get_url(), files=files, data=body)

        # Then the error is returned inside the response as JSON
        assert response.status_code == 400
        assert response.headers.get('content-type') == application_json
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingDiagramFileError'
        assert body_response['title'] == 'Diagram file is not valid'
        assert body_response['detail'] == 'DrawIO processor does not accept diagrams with multiple pages'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'Diagram File is not compatible'

    @pytest.mark.parametrize('diagram_file_path', [
        test_resource_paths.drawio_minimal_xml,
        test_resource_paths.drawio_minimal_drawio,
        test_resource_paths.lean_ix_drawio
    ])
    @responses.activate
    def test_create_otm_ok(self, diagram_file_path):
        # Given a project_id
        project_id: str = 'test_ok'
        project_name: str = 'test_ok_name'

        # And the source file
        diag_file = get_byte_data(diagram_file_path)

        # And the mapping file
        mapping_file = get_byte_data(test_resource_paths.default_drawio_mapping)

        # When I do post on diagram endpoint
        files = {'diag_file': (diagram_file_path, diag_file),
                 'default_mapping_file': ('default_mapping_file.yaml', mapping_file)}
        body = {'diag_type': 'DRAWIO', 'id': project_id, 'name': project_name}
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 201
        assert response.headers.get('content-type') == application_json
        otm = json.loads(response.text)
        assert len(otm['trustZones']) > 0
        assert len(otm['components']) > 0

    @pytest.mark.parametrize('custom_mapping_file_path, expected_component_type', [
        (default_drawio_mapping, 'CD-V2-EMPTY-COMPONENT'), (custom_drawio_mapping, 'vpc')])
    @responses.activate
    def test_custom_mapping_file_override_mapping_file(self, custom_mapping_file_path, expected_component_type):
        # Given a project_id
        project_id: str = 'test_ok'
        project_name: str = 'test_ok_name'

        # And the source file
        diag_file = get_byte_data(drawio_minimal_xml)

        # And the mapping files
        default_mapping_file = get_byte_data(default_drawio_mapping)
        custom_mapping_file = get_byte_data(custom_mapping_file_path)

        # When I do post on diagram endpoint
        files = {'diag_file': (drawio_minimal_xml, diag_file),
                 'default_mapping_file': ('default_mapping_file.yaml', default_mapping_file),
                 'custom_mapping_file': ('custom_mapping_file.yaml', custom_mapping_file)}
        body = {'diag_type': 'DRAWIO', 'id': project_id, 'name': project_name}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == application_json

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'test_ok'
        assert otm['project']['name'] == 'test_ok_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 4
        assert len(otm['dataflows']) == 0
        assert otm['components'][0]['type'] == expected_component_type

    @pytest.mark.parametrize('filepath', [invalid_extension_mtmt_file, terraform_aws_simple_components])
    def test_diagram_file_invalid_extensions(self, filepath):
        # GIVEN a drawio file
        drawio_file = get_byte_data(filepath)

        # AND a mapping file
        mapping_file = get_byte_data(default_drawio_mapping)

        # WHEN I do post on diagram endpoint
        files = {'diag_file': (filepath, drawio_file),
                 'default_mapping_file': ('default_mapping_file.yaml', mapping_file)}
        body = {'diag_type': 'DRAWIO', 'id': "project_id", 'name': "project_name"}
        response = client.post(get_url(), files=files, data=body)

        # AND the error details are correct
        assert response.status_code == 400
        assert response.headers.get('content-type') == application_json

        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'DiagramFileNotValidError'
        assert body_response['title'] == 'Drawio file is not valid'
        assert body_response['detail'] == 'Provided diag_file is not valid. It does not comply with schema'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'Provided diag_file is not valid. It does not comply with schema'
