import json
from http import HTTPStatus

import responses
from fastapi.testclient import TestClient
from pytest import mark, param
from slp_base.slp_base.provider_type import application_json, VALID_YAML_MIME_TYPES

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

def get_file(file_path, mime_type):
    return file_path, open(file_path, 'rb'), mime_type

class TestOTMControllerIaCTFPlan:

    @responses.activate
    @mark.parametrize('custom_mapping_file_path, expected_component_type',
                      [param(terraform_plan_default_mapping_file, 'dynamodb', id='default_as_custom'),
                       param(terraform_plan_custom_mapping_file, 'empty-component', id='custom_overrides_default'),
                       param(None, 'dynamodb', id='no_custom_mapping')
                       ])
    def test_custom_mapping_file(self, custom_mapping_file_path, expected_component_type):
        # Given the provided files (iac, mapping and custom mapping)
        iac_file_plan = get_file(terraform_plan_official, application_json)
        iac_file_graph = get_file(terraform_graph_official, application_json)
        mapping_file = get_file(terraform_plan_default_mapping_file, VALID_YAML_MIME_TYPES[1])
        files = [('iac_file', iac_file_plan), ('iac_file', iac_file_graph),
                 ('mapping_file', mapping_file)]
        if custom_mapping_file_path:
            custom_mapping_file = get_file(custom_mapping_file_path, VALID_YAML_MIME_TYPES[1])
            files.append(('custom_mapping_file', custom_mapping_file))

        # When I do post on Terraform Plan endpoint
        url = iac_create_otm_controller.PREFIX + '/iac'
        body = {'iac_type': TESTING_IAC_TYPE, 'id': PROJECT_ID, 'name': PROJECT_NAME}
        response = client.post(url, files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert HTTPStatus.CREATED == response.status_code
        assert application_json == response.headers.get('content-type')

        otm = json.loads(response.text)
        assert otm['otmVersion'] == '0.2.0'
        assert otm['project']['id'] == 'project_A_id'
        assert otm['project']['name'] == 'project_A_name'
        assert otm['project']['name'] == 'project_A_name'
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 8
        assert len(otm['dataflows']) == 8
        assert otm['components'][0]['type'] == expected_component_type
