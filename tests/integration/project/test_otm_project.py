from unittest.mock import patch

from _pytest.python_api import raises

from startleft.api.errors import OtmBuildingError, OtmResultError
from startleft.otm.otm_project import OtmProject
from startleft.utils import file_utils as FileUtils
from tests.resources import test_resource_paths

SAMPLE_OTM_FILENAME = test_resource_paths.otm_file_example
CUSTOM_YAML_VISIO_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
OTM_FILE_EXAMPLE = test_resource_paths.otm_file_example

MOCK_PROJECT_ID = 'id'
MOCK_PROJECT_NAME = 'name'


class TestOtmProjectService:

    def test_from_otm_id_and_name_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename, project_id, project_name)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == project_name

    def test_from_otm_id_and_name_not_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project id
        project_id = 'id'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename=otm_filename, project_id=project_id)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == otm_project.otm['project']['id']

    def test_from_otm_custom_mapping_files_not_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project name
        project_name = 'name'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename=otm_filename, project_name=project_name)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == otm_project.otm['project']['id']
        assert otm_project.project_name == project_name

    def test_validate_diagram_mappings_file_ok(self):
        # Given a sample valid Mapping Visio file
        mapping_file = [FileUtils.get_data(CUSTOM_YAML_VISIO_MAPPING_FILENAME)]

        # When validating
        # Then validator returns OK
        OtmProject.validate_diagram_mappings_file(mapping_file)

    def test_response_on_otm_nonexistent_file(self):
        # Given a sample valid IaC file
        otm_file = '/tmp/nonexistent.otm'

        # When creating OTM project from IaC file
        # Then raises OtmResultError
        with raises(OtmResultError):
            OtmProject.load_and_validate_otm_file(otm_file)

    @patch('startleft.otm.otm_file_loader.OtmFileLoader.load')
    def test_response_on_otm_loading_error(self, mock_load_source_data):
        # Given a sample valid IaC file
        otm_file = OTM_FILE_EXAMPLE

        # And the mocked method throwing a LoadingIacFileError
        error = OtmBuildingError('OTM file not exists', 'mocked error detail', 'mocked error msg')
        mock_load_source_data.side_effect = error

        # When creating OTM project from IaC file
        # Then raises OtmBuildingError
        with raises(OtmBuildingError):
            OtmProject.load_and_validate_otm_file(otm_file)
