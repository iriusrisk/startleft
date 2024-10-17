import json

import pytest
from fastapi.testclient import TestClient

from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.etm import etm_create_otm_controller

webapp = fastapi_server.webapp

client = TestClient(webapp)


def get_url():
    return etm_create_otm_controller.PREFIX + etm_create_otm_controller.URL


octet_stream = 'application/octet-stream'


class TestOTMControllerEtm:

    @pytest.mark.parametrize("project_id,project_name,source_file,errors_expected, error_type", [
        (None, 'name', None, 4, 'RequestValidationError'),
        ('id', None, None, 4, 'RequestValidationError'),
        ('id', 'name', None, 3, 'RequestValidationError'),
        (None, None, None, 5, 'RequestValidationError'),
        ('', None, None, 5, 'RequestValidationError')
    ])
    def test_create_project_validation_error(self, project_id: str, project_name: str, source_file,
                                             errors_expected: int,
                                             error_type: str):
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
