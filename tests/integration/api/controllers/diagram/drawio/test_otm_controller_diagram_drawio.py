import json

import responses
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
        assert response.headers.get('content-type') == json_mime
        body_response = json.loads(response.text)
        assert body_response['status'] == '400'
        assert body_response['error_type'] == 'LoadingDiagramFileError'
        assert body_response['title'] == 'Diagram file is not valid'
        assert body_response['detail'] == 'DrawIO processor does not accept diagrams with multiple pages'
        assert len(body_response['errors']) == 1
        assert body_response['errors'][0]['errorMessage'] == 'Diagram File is not compatible'