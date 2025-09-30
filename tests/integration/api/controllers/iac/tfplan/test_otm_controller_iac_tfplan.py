import json

import responses
from pytest import mark
from fastapi.testclient import TestClient

from slp_base import IacType
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.iac import iac_create_otm_controller
from tests.resources.test_resource_paths import terraform_plan_official, terraform_graph_official, \
    terraform_plan_default_mapping_file, terraform_plan_custom_mapping_file

TESTING_IAC_TYPE = IacType.TFPLAN.value

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'
yaml_mime = 'text/yaml'

def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL

class TestOTMControllerIaCTFPlan:

    @responses.activate
    @mark.parametrize('custom_mapping_file_path, expected_component_type',
                      [(terraform_plan_default_mapping_file, 'dynamodb'),
                       (terraform_plan_custom_mapping_file, 'empty-component')])
    def test_custom_mapping_file_override_mapping_file(self, custom_mapping_file_path, expected_component_type):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the provided files (iac, mapping and custom mapping)
        iac_file_plan = (terraform_plan_official, open(terraform_plan_official, 'rb'), json_mime)
        iac_file_graph = (terraform_graph_official, open(terraform_graph_official, 'rb'), json_mime)
        mapping_file = (terraform_plan_default_mapping_file, open(terraform_plan_default_mapping_file, 'rb'), yaml_mime)
        custom_mapping_file = (custom_mapping_file_path, open(custom_mapping_file_path, 'rb'), yaml_mime)
        files = [('iac_file', iac_file_plan), ('iac_file', iac_file_graph),
                 ('mapping_file', mapping_file), ('custom_mapping_file', custom_mapping_file) ]

        # When I do post on cloudformation endpoint
        body = {'iac_type': TESTING_IAC_TYPE, 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == json_mime

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 8
        assert len(otm['dataflows']) == 8
        assert otm['components'][0]['type'] == expected_component_type
