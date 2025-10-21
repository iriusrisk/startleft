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
PROJECT_ID = 'project_A_id'
PROJECT_NAME = 'project_A_name'

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'
yaml_mime = 'text/yaml'

def get_file(file_path, mime_type):
    return file_path, open(file_path, 'rb'), mime_type

def get_response(files, iac_type, project_id, project_name):
    url = iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL
    body = {'iac_type': iac_type, 'id': project_id, 'name': project_name}
    return client.post(url, files=files, data=body)

def assert_success_response(response):
    assert iac_create_otm_controller.RESPONSE_STATUS_CODE == response.status_code
    assert json_mime == response.headers.get('content-type')

class TestOTMControllerIaCTFPlan:
    def test_tfplan_happy_path_no_custom_mapping(self):
        # Given the provided files (iacs and mapping)
        iac_file_plan = get_file(terraform_plan_official, json_mime)
        iac_file_graph = get_file(terraform_graph_official, json_mime)
        mapping_file = get_file(terraform_plan_default_mapping_file, yaml_mime)
        files = [('iac_file', iac_file_plan), ('iac_file', iac_file_graph), ('mapping_file', mapping_file) ]

        # When I do post on Terraform Plan endpoint
        response = get_response(files, TESTING_IAC_TYPE, PROJECT_ID, PROJECT_NAME)

        # Then the OTM is returned inside the response as JSON
        assert_success_response(response)

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 8
        assert len(otm['dataflows']) == 8
        assert otm['components'][0]['type'] == 'dynamodb'

    @responses.activate
    @mark.parametrize('custom_mapping_file_path, expected_component_type',
                      [(terraform_plan_default_mapping_file, 'dynamodb'),
                       (terraform_plan_custom_mapping_file, 'empty-component')])
    def test_custom_mapping_file_override_mapping_file(self, custom_mapping_file_path, expected_component_type):
        # Given the provided files (iac, mapping and custom mapping)
        iac_file_plan = get_file(terraform_plan_official, json_mime)
        iac_file_graph = get_file(terraform_graph_official, json_mime)
        mapping_file = get_file(terraform_plan_default_mapping_file, yaml_mime)
        custom_mapping_file = get_file(custom_mapping_file_path, yaml_mime)
        files = [('iac_file', iac_file_plan), ('iac_file', iac_file_graph),
                 ('mapping_file', mapping_file), ('custom_mapping_file', custom_mapping_file) ]

        # When I do post on Terraform Plan endpoint
        response = get_response(files, TESTING_IAC_TYPE, PROJECT_ID, PROJECT_NAME)

        # Then the OTM is returned inside the response as JSON
        assert_success_response(response)

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 8
        assert len(otm['dataflows']) == 8
        assert otm['components'][0]['type'] == expected_component_type
