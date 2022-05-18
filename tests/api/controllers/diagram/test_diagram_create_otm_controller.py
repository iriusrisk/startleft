import json

import pytest
import responses
from fastapi.testclient import TestClient

from startleft.api import fastapi_server
from startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources import test_resource_paths

IRIUSRISK_URL = ''

webapp = fastapi_server.initialize_webapp(IRIUSRISK_URL)

client = TestClient(webapp)


def get_url():
    return diag_create_otm_controller.PREFIX + diag_create_otm_controller.URL


class TestDiagramCreateOtmController:

    @pytest.mark.parametrize('project_id,project_name,diag_file,errors_expected',
                             [(None, 'name', open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'), 3),
                              ('id', None, open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'), 3),
                              ('id', 'name', None, 3),
                              ('id', None, None, 4),
                              (None, 'name', None, 4),
                              ('', None, None, 5)])
    def test_create_project_validation_error(self, project_id: str, project_name: str, diag_file, errors_expected: int):
        # Given a body
        body = {'id': project_id, 'name': project_name}

        # When I do post on cloudformation endpoint
        files = {'diag_file': diag_file}
        response = client.post(get_url(), files=files, data=body)

        # Then
        assert response.status_code == 400
        error = json.loads(response.text)
        assert error['status'] == 'error'
        assert len(error['errors']) == errors_expected
        for e in error['errors']:
            assert len(e['errorMessage']) > 0

    @responses.activate
    def test_create_otm_ok(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on cloudformation endpoint
        files = {'diag_file': open(test_resource_paths.visio_aws_with_tz_and_vpc, 'rb'),
                 'mapping_file': open(test_resource_paths.default_visio_mapping, 'rb')}
        body = {'diag_type': 'VISIO', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        otm = json.loads(response.text)

        assert otm['otmVersion'] == '0.1.0'
        assert otm['project']['id'] == project_id
        assert otm['project']['name'] == 'project_A_name'

        assert len(otm['representations']) == 1

        assert otm['representations'][0]['name'] == 'Visio'
        assert otm['representations'][0]['id'] == 'Visio'
        assert otm['representations'][0]['type'] == 'diagram'

        assert len(otm['trustZones']) == 2

        assert otm['trustZones'][0]['id'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['trustZones'][0]['name'] == 'Public Cloud'
        assert len(otm['trustZones'][0]['risk']) == 1
        assert otm['trustZones'][0]['risk']['trustRating'] == 10
        assert otm['trustZones'][1]['id'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm['trustZones'][1]['name'] == 'Private Secured'
        assert len(otm['trustZones'][1]['risk']) == 1
        assert otm['trustZones'][1]['risk']['trustRating'] == 10

        assert len(otm['components']) == 5

        assert otm['components'][0]['id'] == '1'
        assert otm['components'][0]['name'] == 'Amazon EC2'
        assert otm['components'][0]['type'] == 'ec2'
        assert len(otm['components'][0]['parent']) == 1
        assert otm['components'][0]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][1]['id'] == '12'
        assert otm['components'][1]['name'] == 'Custom machine'
        assert otm['components'][1]['type'] == 'ec2'
        assert len(otm['components'][1]['parent']) == 1
        assert otm['components'][1]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][2]['id'] == '30'
        assert otm['components'][2]['name'] == 'Private Database'
        assert otm['components'][2]['type'] == 'rds'
        assert len(otm['components'][2]['parent']) == 1
        assert otm['components'][2]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

        assert otm['components'][3]['id'] == '35'
        assert otm['components'][3]['name'] == 'Amazon CloudWatch'
        assert otm['components'][3]['type'] == 'cloudwatch'
        assert len(otm['components'][3]['parent']) == 1
        assert otm['components'][3]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][4]['id'] == '41'
        assert otm['components'][4]['name'] == 'Custom log system'
        assert otm['components'][4]['type'] == 'cloudwatch'
        assert len(otm['components'][4]['parent']) == 1
        assert otm['components'][4]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert len(otm['dataflows']) == 4

        assert otm['dataflows'][0]['id'] == '17'
        assert len(otm['dataflows'][0]['name']) == 36
        assert otm['dataflows'][0]['source'] == '1'
        assert otm['dataflows'][0]['destination'] == '12'
        assert otm['dataflows'][1]['id'] == '34'
        assert len(otm['dataflows'][1]['name']) == 36
        assert otm['dataflows'][1]['source'] == '12'
        assert otm['dataflows'][1]['destination'] == '30'
        assert otm['dataflows'][2]['id'] == '40'
        assert len(otm['dataflows'][2]['name']) == 36
        assert otm['dataflows'][2]['source'] == '1'
        assert otm['dataflows'][2]['destination'] == '35'
        assert otm['dataflows'][3]['id'] == '46'
        assert len(otm['dataflows'][3]['name']) == 36
        assert otm['dataflows'][3]['source'] == '12'
        assert otm['dataflows'][3]['destination'] == '41'
