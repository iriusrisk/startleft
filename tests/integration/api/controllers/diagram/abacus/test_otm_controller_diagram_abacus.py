import json

import responses
from fastapi.testclient import TestClient

from sl_util.sl_util.file_utils import get_byte_data
from slp_base.slp_base.otm_validator import OTMValidator
from slp_base.slp_base.provider_type import application_json
from slp_base.slp_base.schema import Schema
from startleft.startleft.api import fastapi_server
from tests.integration.api.controllers.diagram.test_otm_controller_diagram import get_url
from tests.resources import test_resource_paths

webapp = fastapi_server.webapp
client = TestClient(webapp)

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_FILE = test_resource_paths.abacus_example
SAMPLE_DEFAULT_MAPPING = test_resource_paths.abacus_default_mapping
SAMPLE_CUSTOM_MAPPING = test_resource_paths.abacus_custom_mapping

OTM_SCHEMA_FILENAME = OTMValidator.schema_filename


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

        # AND the OTM is valid according to the OTM schema
        schema: Schema = Schema.from_package('otm', OTM_SCHEMA_FILENAME)
        schema.validate(otm)
        assert schema.valid, f"OTM Schema is not valid: {schema.errors}"

        # AND the OTM contains expected data
        assert len(otm['representations']) == 1
        assert len(otm['trustZones']) == 1
        assert len(otm['dataflows']) == 0
        components = otm['components']
        assert len(components) == 8
        assert components[0]['type'] == 'compact-server-side-web-application'
        assert components[1]['type'] == 'CD-MSG-BROKER'
        assert components[2]['type'] == 'back-end-server'
        assert components[3]['type'] == 'other-database'
        assert components[4]['type'] == 'CD-CONTENT-DELIVERY-NETWORK'
        assert components[5]['type'] == 'compact-server-side-web-application'
        assert components[6]['type'] == 'compact-server-side-web-application'
        assert components[7]['type'] == 'web-client'

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
        assert len(otm['dataflows']) == 0
        components = otm['components']
        assert len(components) == 7
        assert components[0]['type'] == 'CD-V2-SST-POC-WEBPAGE'
        assert components[1]['type'] == 'CD-V2-SST-POC-INTEGRATOR'
        assert components[2]['type'] == 'back-end-server'
        assert components[3]['type'] == 'other-database'
        assert components[4]['type'] == 'CD-V2-SST-POC-WEBPAGE'
        assert components[5]['type'] == 'CD-V2-SST-POC-WEBPAGE'
        assert components[6]['type'] == 'web-client'
