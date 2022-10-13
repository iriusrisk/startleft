import json

import pytest
from fastapi.testclient import TestClient

from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources import test_resource_paths

IRIUSRISK_URL = ''

webapp = fastapi_server.initialize_webapp()

client = TestClient(webapp)


def get_url():
    return diag_create_otm_controller.PREFIX + diag_create_otm_controller.URL


octet_stream = 'application/octet-stream'


class TestOtmControllerDiagram:

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
        files = {'diag_file': diag_file}
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        res_body = json.loads(response.text)
        assert res_body['status'] == '400'
        assert res_body['error_type'] == error_type
        assert len(res_body['errors']) == errors_expected
        for e in res_body['errors']:
            assert len(e['errorMessage']) > 0
