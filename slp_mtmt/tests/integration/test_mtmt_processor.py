from sl_util.sl_util.file_utils import get_byte_data
from slp_mtmt import MTMTProcessor
from slp_mtmt.tests.resources import test_resource_paths

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mapping_mtmt_mvp


class TestMtmtProcessor:

    def test_run_valid_mappings(self):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(SAMPLE_VALID_MTMT_FILE)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 0

        # AND the info inside trustzones is also right
        assert len(otm.trustzones) == 2
        trustzone = otm.trustzones[0]
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        trustzone = otm.trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'

        # AND the info inside components is also right
        assert len(otm.components) == 4
        component = otm.components[0]
        assert component.id == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert component.name == 'Accounting PostgreSQL'
        assert component.type == 'CD-MICROSOFT-AZURE-DB-POSTGRESQL'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        component = otm.components[1]
        assert component.id == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert component.name == 'Mobile Client'
        assert component.type == 'android-device-client'
        assert component.parent == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        component = otm.components[2]
        assert component.id == '5d15323e-3729-4694-87b1-181c90af5045'
        assert component.name == 'Public API v2'
        assert component.type == 'rest-full-web-service'
        assert component.parent == "24cdf4da-ac7f-4a35-bab0-29256d4169bf"
        component = otm.components[3]
        assert component.id == '91882aca-8249-49a7-96f0-164b68411b48'
        assert component.name == 'Azure File Storage'
        assert component.type == 'azure-storage'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
