import json
from unittest.mock import patch

import responses
from fastapi.testclient import TestClient
from pytest import mark

from sl_util.sl_util.file_utils import get_byte_data
from slp_base.slp_base.errors import DiagramFileNotValidError, MappingFileNotValidError, LoadingMappingFileError, \
    OtmResultError, OtmBuildingError, LoadingDiagramFileError
from slp_visio.tests.unit.util.test_uuid import is_valid_uuid
from startleft.startleft.api import fastapi_server
from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from tests.resources import test_resource_paths
from tests.resources.test_resource_paths import visio_aws_with_tz_and_vpc, default_visio_mapping, \
    custom_vpc_mapping

IRIUSRISK_URL = ''

webapp = fastapi_server.webapp

client = TestClient(webapp)


def get_url():
    return diag_create_otm_controller.PREFIX + diag_create_otm_controller.URL


octet_stream = 'application/octet-stream'


class TestOtmControllerDiagramLucid:

    @responses.activate
    def test_create_otm_ok_lucid_aws_with_tz(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the source file
        diag_file = get_byte_data(test_resource_paths.lucid_aws_with_tz)

        # And the mapping files
        mapping_file = get_byte_data(test_resource_paths.default_lucid_mapping)
        custom_mapping_file = get_byte_data(test_resource_paths.lucid_aws_with_tz_mapping)

        # When I do post on diagram endpoint
        files = {'diag_file': diag_file,
                 'default_mapping_file': mapping_file,
                 'custom_mapping_file': custom_mapping_file
                 }
        body = {'diag_type': 'LUCID', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        otm = json.loads(response.text)

        assert otm['otmVersion'] == '0.1.0'
        assert otm['project']['id'] == project_id
        assert otm['project']['name'] == 'project_A_name'

        assert len(otm['representations']) == 1

        assert otm['representations'][0]['name'] == f'{project_id} Diagram Representation'
        assert otm['representations'][0]['id'] == f'{project_id}-diagram'
        assert otm['representations'][0]['type'] == 'diagram'
        assert otm['representations'][0]['size']['width'] == 2378
        assert otm['representations'][0]['size']['height'] == 1558

        assert len(otm['trustZones']) == 3

        assert otm['trustZones'][0]['id'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['trustZones'][0]['name'] == 'Public Cloud'
        assert len(otm['trustZones'][0]['risk']) == 1
        assert otm['trustZones'][0]['risk']['trustRating'] == 10
        assert otm['trustZones'][1]['id'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm['trustZones'][1]['name'] == 'Private Secured Cloud'
        assert len(otm['trustZones'][1]['risk']) == 1
        assert otm['trustZones'][1]['risk']['trustRating'] == 10
        assert otm['trustZones'][2]['id'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert otm['trustZones'][2]['name'] == 'Internet'
        assert len(otm['trustZones'][2]['risk']) == 1
        assert otm['trustZones'][2]['risk']['trustRating'] == 10

        assert len(otm['components']) == 9

        assert otm['components'][0]['id'] == '7'
        assert otm['components'][0]['name'] == 'My EC2'
        assert otm['components'][0]['type'] == 'ec2'
        assert len(otm['components'][0]['parent']) == 1
        assert otm['components'][0]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][1]['id'] == '10'
        assert otm['components'][1]['name'] == 'My CloudWatch'
        assert otm['components'][1]['type'] == 'cloudwatch'
        assert len(otm['components'][1]['parent']) == 1
        assert otm['components'][1]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][2]['id'] == '15'
        assert otm['components'][2]['name'] == 'My API Gateway'
        assert otm['components'][2]['type'] == 'api-gateway'
        assert len(otm['components'][2]['parent']) == 1
        assert otm['components'][2]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][3]['id'] == '24'
        assert otm['components'][3]['name'] == 'My CloudTrail'
        assert otm['components'][3]['type'] == 'cloudtrail'
        assert len(otm['components'][3]['parent']) == 1
        assert otm['components'][3]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][4]['id'] == '27'
        assert otm['components'][4]['name'] == 'My Simple Storage Service (S3)'
        assert otm['components'][4]['type'] == 's3'
        assert len(otm['components'][4]['parent']) == 1
        assert otm['components'][4]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][5]['id'] == '36'
        assert otm['components'][5]['name'] == 'Web browser'
        assert otm['components'][5]['type'] == 'generic-client'
        assert len(otm['components'][5]['parent']) == 1
        assert otm['components'][5]['parent']['trustZone'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

        assert otm['components'][6]['id'] == '42'
        assert otm['components'][6]['name'] == 'Android'
        assert otm['components'][6]['type'] == 'android-device-client'
        assert len(otm['components'][6]['parent']) == 1
        assert otm['components'][6]['parent']['trustZone'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

        assert otm['components'][7]['id'] == '45'
        assert otm['components'][7]['name'] == 'SQL Database'
        assert otm['components'][7]['type'] == 'CD-MICROSOFT-AZURE-SQL-DB'
        assert len(otm['components'][7]['parent']) == 1
        assert otm['components'][7]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

        assert otm['components'][8]['id'] == '51'
        assert otm['components'][8]['name'] == 'My DynamoDB'
        assert otm['components'][8]['type'] == 'dynamodb'
        assert len(otm['components'][8]['parent']) == 1
        assert otm['components'][8]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

        assert len(otm['dataflows']) == 8

        assert otm['dataflows'][0]['id'] == '30'
        assert otm['dataflows'][0]['name'] == 'EC2 Logs'
        assert otm['dataflows'][0]['source'] == '7'
        assert otm['dataflows'][0]['destination'] == '10'

        assert otm['dataflows'][1]['id'] == '31'
        assert otm['dataflows'][1]['name'] == 'GW/EC2'
        assert otm['dataflows'][1]['source'] == '15'
        assert otm['dataflows'][1]['destination'] == '7'

        assert otm['dataflows'][2]['id'] == '32'
        assert otm['dataflows'][2]['name'] == 'Log trace'
        assert otm['dataflows'][2]['source'] == '15'
        assert otm['dataflows'][2]['destination'] == '24'

        assert otm['dataflows'][3]['id'] == '33'
        assert otm['dataflows'][3]['name'] == 'Customer data'
        assert otm['dataflows'][3]['source'] == '15'
        assert otm['dataflows'][3]['destination'] == '27'

        assert otm['dataflows'][4]['id'] == '41'
        assert len(otm['dataflows'][4]['name']) == 36
        assert otm['dataflows'][4]['source'] == '36'
        assert otm['dataflows'][4]['destination'] == '15'

        assert otm['dataflows'][5]['id'] == '44'
        assert len(otm['dataflows'][5]['name']) == 36
        assert otm['dataflows'][5]['source'] == '42'
        assert otm['dataflows'][5]['destination'] == '15'

        assert otm['dataflows'][6]['id'] == '54'
        assert otm['dataflows'][6]['name'] == 'User data'
        assert otm['dataflows'][6]['source'] == '15'
        assert otm['dataflows'][6]['destination'] == '51'

        assert otm['dataflows'][7]['id'] == '55'
        assert otm['dataflows'][7]['name'] == 'App data'
        assert otm['dataflows'][7]['source'] == '15'
        assert otm['dataflows'][7]['destination'] == '45'

    @responses.activate
    def test_create_otm_ok_lucid_aws_with_tz_and_vpc(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # And the source file
        diag_file = get_byte_data(test_resource_paths.lucid_aws_with_tz_and_vpc)

        # And the mapping files
        mapping_file = get_byte_data(test_resource_paths.default_lucid_mapping)
        custom_mapping_file = get_byte_data(test_resource_paths.lucid_aws_with_tz_and_vpc_mapping)

        # When I do post on diagram endpoint
        files = {'diag_file': diag_file,
                 'default_mapping_file': mapping_file,
                 'custom_mapping_file': custom_mapping_file
                 }
        body = {'diag_type': 'LUCID', 'id': f'{project_id}', 'name': 'project_A_name'}
        response = client.post(get_url(), files=files, data=body)

        # Then the OTM is returned inside the response as JSON
        assert response.status_code == diag_create_otm_controller.RESPONSE_STATUS_CODE
        assert response.headers.get('content-type') == 'application/json'
        otm = json.loads(response.text)

        assert otm['otmVersion'] == '0.1.0'
        assert otm['project']['id'] == project_id
        assert otm['project']['name'] == 'project_A_name'

        assert len(otm['representations']) == 1

        assert otm['representations'][0]['name'] == f'{project_id} Diagram Representation'
        assert otm['representations'][0]['id'] == f'{project_id}-diagram'
        assert otm['representations'][0]['type'] == 'diagram'
        assert otm['representations'][0]['size']['width'] == 2378
        assert otm['representations'][0]['size']['height'] == 1558

        assert len(otm['trustZones']) == 3

        assert otm['trustZones'][0]['id'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['trustZones'][0]['name'] == 'Public Cloud'
        assert len(otm['trustZones'][0]['risk']) == 1
        assert otm['trustZones'][0]['risk']['trustRating'] == 10
        assert otm['trustZones'][1]['id'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm['trustZones'][1]['name'] == 'Private Secured Cloud'
        assert len(otm['trustZones'][1]['risk']) == 1
        assert otm['trustZones'][1]['risk']['trustRating'] == 10
        assert otm['trustZones'][2]['id'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert otm['trustZones'][2]['name'] == 'Internet'
        assert len(otm['trustZones'][2]['risk']) == 1
        assert otm['trustZones'][2]['risk']['trustRating'] == 10

        assert len(otm['components']) == 10

        assert otm['components'][0]['id'] == '7'
        assert otm['components'][0]['name'] == 'Custom VPC'
        assert otm['components'][0]['type'] == 'empty-component'
        assert len(otm['components'][0]['parent']) == 1
        assert otm['components'][0]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][1]['id'] == '9'
        assert otm['components'][1]['name'] == 'My EC2'
        assert otm['components'][1]['type'] == 'ec2'
        assert len(otm['components'][1]['parent']) == 1
        assert otm['components'][1]['parent']['component'] == '7'

        assert otm['components'][2]['id'] == '12'
        assert otm['components'][2]['name'] == 'My CloudWatch'
        assert otm['components'][2]['type'] == 'cloudwatch'
        assert len(otm['components'][2]['parent']) == 1
        assert otm['components'][2]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][3]['id'] == '17'
        assert otm['components'][3]['name'] == 'My API Gateway'
        assert otm['components'][3]['type'] == 'api-gateway'
        assert len(otm['components'][3]['parent']) == 1
        assert otm['components'][3]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][4]['id'] == '26'
        assert otm['components'][4]['name'] == 'My CloudTrail'
        assert otm['components'][4]['type'] == 'cloudtrail'
        assert len(otm['components'][4]['parent']) == 1
        assert otm['components'][4]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][5]['id'] == '29'
        assert otm['components'][5]['name'] == 'My Simple Storage Service (S3)'
        assert otm['components'][5]['type'] == 's3'
        assert len(otm['components'][5]['parent']) == 1
        assert otm['components'][5]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

        assert otm['components'][6]['id'] == '38'
        assert otm['components'][6]['name'] == 'Web browser'
        assert otm['components'][6]['type'] == 'generic-client'
        assert len(otm['components'][6]['parent']) == 1
        assert otm['components'][6]['parent']['trustZone'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

        assert otm['components'][7]['id'] == '44'
        assert otm['components'][7]['name'] == 'Android'
        assert otm['components'][7]['type'] == 'android-device-client'
        assert len(otm['components'][7]['parent']) == 1
        assert otm['components'][7]['parent']['trustZone'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

        assert otm['components'][8]['id'] == '47'
        assert otm['components'][8]['name'] == 'SQL Database'
        assert otm['components'][8]['type'] == 'CD-MICROSOFT-AZURE-SQL-DB'
        assert len(otm['components'][8]['parent']) == 1
        assert otm['components'][8]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

        assert otm['components'][9]['id'] == '53'
        assert otm['components'][9]['name'] == 'My DynamoDB'
        assert otm['components'][9]['type'] == 'dynamodb'
        assert len(otm['components'][9]['parent']) == 1
        assert otm['components'][9]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

        assert len(otm['dataflows']) == 8

        assert otm['dataflows'][0]['id'] == '32'
        assert otm['dataflows'][0]['name'] == 'EC2 Logs'
        assert otm['dataflows'][0]['source'] == '9'
        assert otm['dataflows'][0]['destination'] == '12'

        assert otm['dataflows'][1]['id'] == '33'
        assert otm['dataflows'][1]['name'] == 'GW/EC2'
        assert otm['dataflows'][1]['source'] == '17'
        assert otm['dataflows'][1]['destination'] == '9'

        assert otm['dataflows'][2]['id'] == '34'
        assert otm['dataflows'][2]['name'] == 'Log trace'
        assert otm['dataflows'][2]['source'] == '17'
        assert otm['dataflows'][2]['destination'] == '26'

        assert otm['dataflows'][3]['id'] == '35'
        assert otm['dataflows'][3]['name'] == 'Customer data'
        assert otm['dataflows'][3]['source'] == '17'
        assert otm['dataflows'][3]['destination'] == '29'

        assert otm['dataflows'][4]['id'] == '43'
        assert is_valid_uuid((otm['dataflows'][4]['name']))
        assert otm['dataflows'][4]['source'] == '38'
        assert otm['dataflows'][4]['destination'] == '17'

        assert otm['dataflows'][5]['id'] == '46'
        assert is_valid_uuid(otm['dataflows'][5]['name'])
        assert otm['dataflows'][5]['source'] == '44'
        assert otm['dataflows'][5]['destination'] == '17'

        assert otm['dataflows'][6]['id'] == '56'
        assert otm['dataflows'][6]['name'] == 'User data'
        assert otm['dataflows'][6]['source'] == '17'
        assert otm['dataflows'][6]['destination'] == '53'

        assert otm['dataflows'][7]['id'] == '57'
        assert otm['dataflows'][7]['name'] == 'App data'
        assert otm['dataflows'][7]['source'] == '17'
        assert otm['dataflows'][7]['destination'] == '47'

    @responses.activate
    def test_create_otm_ok_both_mapping_files(self):
        # Given a project_id
        project_id: str = 'project_A_id'

        # When I do post on diagram endpoint
        files = {'diag_file': open(visio_aws_with_tz_and_vpc, 'rb'),
                 'default_mapping_file': open(default_visio_mapping, 'rb'),
                 'custom_mapping_file': open(custom_vpc_mapping, 'rb')}
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
        assert otm['representations'][0]['name'] == f'{project_id} Diagram Representation'
        assert otm['representations'][0]['id'] == f'{project_id}-diagram'
        assert otm['representations'][0]['type'] == 'diagram'
        assert otm['representations'][0]['size']['width'] == 1967
        assert otm['representations'][0]['size']['height'] == 1356
        assert len(otm['trustZones']) == 2
        assert otm['trustZones'][0]['id'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['trustZones'][0]['name'] == 'Public Cloud'
        assert len(otm['trustZones'][0]['risk']) == 1
        assert otm['trustZones'][0]['risk']['trustRating'] == 10
        assert otm['trustZones'][1]['id'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm['trustZones'][1]['name'] == 'Private Secured Cloud'
        assert len(otm['trustZones'][1]['risk']) == 1
        assert otm['trustZones'][1]['risk']['trustRating'] == 10
        assert len(otm['components']) == 6
        assert otm['components'][0]['id'] == '49'
        assert otm['components'][0]['name'] == 'Custom VPC'
        assert otm['components'][0]['type'] == 'empty-component'
        assert len(otm['components'][0]['parent']) == 1
        assert otm['components'][0]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['components'][1]['id'] == '1'
        assert otm['components'][1]['name'] == 'Amazon EC2'
        assert otm['components'][1]['type'] == 'ec2'
        assert len(otm['components'][1]['parent']) == 1
        assert otm['components'][1]['parent']['component'] == '49'
        assert otm['components'][2]['id'] == '12'
        assert otm['components'][2]['name'] == 'Custom machine'
        assert otm['components'][2]['type'] == 'ec2'
        assert len(otm['components'][2]['parent']) == 1
        assert otm['components'][2]['parent']['component'] == '49'
        assert otm['components'][3]['id'] == '30'
        assert otm['components'][3]['name'] == 'Private Database'
        assert otm['components'][3]['type'] == 'rds'
        assert len(otm['components'][3]['parent']) == 1
        assert otm['components'][3]['parent']['trustZone'] == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm['components'][4]['id'] == '35'
        assert otm['components'][4]['name'] == 'Amazon CloudWatch'
        assert otm['components'][4]['type'] == 'cloudwatch'
        assert len(otm['components'][4]['parent']) == 1
        assert otm['components'][4]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm['components'][5]['id'] == '41'
        assert otm['components'][5]['name'] == 'Custom log system'
        assert otm['components'][5]['type'] == 'cloudwatch'
        assert len(otm['components'][5]['parent']) == 1
        assert otm['components'][5]['parent']['trustZone'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
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
        mapping_source = bytes(mapping_source) if isinstance(mapping_source, bytearray) else mapping_source
        diagram_file = (visio_aws_with_tz_and_vpc, open(visio_aws_with_tz_and_vpc, 'rb'), 'application/json')
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
