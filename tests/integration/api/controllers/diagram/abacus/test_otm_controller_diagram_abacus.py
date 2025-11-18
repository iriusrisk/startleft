import json
import responses
from fastapi.testclient import TestClient
from slp_base.slp_base.provider_type import application_json
from tests.integration.api.controllers.diagram.test_otm_controller_diagram import get_url
from tests.resources import test_resource_paths
from sl_util.sl_util.file_utils import get_byte_data
from startleft.startleft.api import fastapi_server

webapp = fastapi_server.webapp
client = TestClient(webapp)

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_FILE = test_resource_paths.abacus_example
SAMPLE_DEFAULT_MAPPING = test_resource_paths.abacus_default_mapping
SAMPLE_CUSTOM_MAPPING = test_resource_paths.abacus_custom_mapping

class TestOTMControllerDiagramAbacus:
    @responses.activate
    def test_create_otm_ok_default_mapping(self):
        # GIVEN a source file
        diag_file = get_byte_data(SAMPLE_VALID_FILE)

        # AND a valid default mapping file
        default_mapping_file = get_byte_data(SAMPLE_DEFAULT_MAPPING)

        # WHEN processing
        file = {'diag_file': (SAMPLE_VALID_FILE, diag_file),
                'default_mapping_file': (SAMPLE_DEFAULT_MAPPING, default_mapping_file)}
        body = {'diag_type': 'ABACUS', 'id': SAMPLE_ID, 'name': SAMPLE_NAME}
        response = client.post(get_url(), files=file, data=body)

        # THEN the OTM is returned inside the response as valid JSON
        assert response.status_code == 201
        assert response.headers.get('content-type') == application_json
        otm = json.loads(response.text)
        assert len(otm['representations']) == 1
        assert len(otm['trustZones']) == 1
        assert len(otm['components']) == 8
        assert len(otm['dataflows']) == 0

    def test_create_otm_ok_custom_mapping(self):
        # GIVEN a source file
        diag_file = get_byte_data(SAMPLE_VALID_FILE)

        # AND a valid default mapping file
        default_mapping_file = get_byte_data(SAMPLE_DEFAULT_MAPPING)

        # AND a valid custom mapping file
        custom_mapping_file = get_byte_data(SAMPLE_CUSTOM_MAPPING)

        # WHEN processing
        file = {'diag_file': (SAMPLE_VALID_FILE, diag_file),
                'default_mapping_file': (SAMPLE_DEFAULT_MAPPING, default_mapping_file),
                'custom_mapping_file': (SAMPLE_CUSTOM_MAPPING, custom_mapping_file)}
        body = {'diag_type': 'ABACUS', 'id': SAMPLE_ID, 'name': SAMPLE_NAME}
        response = client.post(get_url(), files=file, data=body)

        # THEN the OTM is returned inside the response as valid JSON
        assert response.status_code == 201
        assert response.headers.get('content-type') == application_json
        otm = json.loads(response.text)
        assert len(otm['representations']) == 1
        assert len(otm['trustZones']) == 2
        assert len(otm['components']) == 7
        assert len(otm['dataflows']) == 0