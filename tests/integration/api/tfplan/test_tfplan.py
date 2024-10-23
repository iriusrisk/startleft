import json

from fastapi.testclient import TestClient

from sl_util.sl_util.file_utils import get_byte_data
from slp_base import IacType
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.iac import iac_create_otm_controller
from tests.resources.test_resource_paths import tfplan_singleton_behaviour_group_by_category, \
    tfplan_ingesting_logs_plan, tfplan_ingesting_logs_graph, tfplan_singleton_behaviour

webapp = fastapi_server.webapp
client = TestClient(webapp)

json_mime = 'application/json'
yaml_mime = 'text/yaml'
DEFAULT_BODY = {'iac_type': IacType.TFPLAN.value, 'id': 'id', 'name': 'name'}

def get_url():
    return iac_create_otm_controller.PREFIX + iac_create_otm_controller.URL

def __files(tfplan, tfgraph, mapping_file):
    return [
        ('iac_file', (tfplan, get_byte_data(tfplan), json_mime)),
        ('iac_file', (tfgraph, get_byte_data(tfgraph), json_mime)),
        ('mapping_file', (mapping_file, get_byte_data(mapping_file), yaml_mime))
    ]

def __extract_and_order_components(otm):
    return sorted(otm['components'], key=lambda x: x['id'])

def test_singleton():
    # GIVEN the mapping file with the singleton behaviour
    files = __files(tfplan_ingesting_logs_plan, tfplan_ingesting_logs_graph, tfplan_singleton_behaviour)

    # WHEN the request is made
    response = client.post(get_url(), files=files, data=DEFAULT_BODY)

    # THEN the response is OK
    assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE

    # AND the resources are grouped by type
    otm = json.loads(response.content.decode('utf-8'))
    components = __extract_and_order_components(otm)
    assert len(components) == 1
    # first component is the API GateWay grouped by regex
    assert components[0]['id'] == 'aws_iam_policy.click_loggerlambda_logging_policy'
    assert components[0]['name'] == 'iam (grouped)'
    assert components[0]['type'] == 'iam'

def test_singleton_grouped_by_category():
    # GIVEN the mapping file with the behaviour group by category configured
    files = __files(tfplan_ingesting_logs_plan, tfplan_ingesting_logs_graph, tfplan_singleton_behaviour_group_by_category)

    # WHEN the request is made
    response = client.post(get_url(), files=files, data=DEFAULT_BODY)

    # THEN the response is OK
    assert response.status_code == iac_create_otm_controller.RESPONSE_STATUS_CODE

    # AND the resources are grouped by category
    otm = json.loads(response.content.decode('utf-8'))
    components = __extract_and_order_components(otm)
    assert len(components) == 2
    # first component is the API GateWay grouped by regex
    assert components[0]['id'] == 'aws_api_gateway_account.click_logger_api_gateway_account'
    assert components[0]['name'] == 'API Gateway'
    assert components[0]['type'] == 'api-gateway'
    # second component is the CloudWatch Log Group grouped by array
    assert components[1]['id'] == 'aws_cloudwatch_log_group.click_logger_firehose_delivery_stream_log_group'
    assert components[1]['name'] == 'CloudWatch'
    assert components[1]['type'] == 'cloudwatch'

