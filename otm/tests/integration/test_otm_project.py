from otm.tests.resources import test_resource_paths
from sl_util.sl_util import file_utils as FileUtils
from startleft.startleft.otm_project import OtmProject

SAMPLE_OTM_FILENAME = test_resource_paths.otm_file_example
CUSTOM_YAML_VISIO_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
OTM_FILE_EXAMPLE = test_resource_paths.otm_file_example

MOCK_PROJECT_ID = 'id'
MOCK_PROJECT_NAME = 'name'


class TestOtmProjectService:

    def test_validate_diagram_mappings_file_ok(self):
        # Given a sample valid Mapping Visio file
        mapping_file = [FileUtils.get_data(CUSTOM_YAML_VISIO_MAPPING_FILENAME)]

        # When validating
        # Then validator returns OK
        OtmProject.validate_diagram_mappings_file(mapping_file)
