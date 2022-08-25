from tests.resources.test_resource_paths import custom_mtmt_single_mapping_file, custom_mtmt_multiple_mapping_file
from startleft.processors.mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader

class TestMTMTMappingLoader:

    def test_mtmt_mapping_loader_happy_path_single_elements(self):

        # GIVEN a mapping file with a trustzone
        # AND a single component
        default_mapping_file = (custom_mtmt_single_mapping_file, open(custom_mtmt_single_mapping_file, 'r'), 'text/yaml')

        # WHEN the load method of the MTMTMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader(default_mapping_file, None)
        mtmt_mapping_file_loader.load()

        # THEN a MTMTMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.trustzones) == 1
        assert len(mtmt_mapping.components) == 1
        assert len(mtmt_mapping.dataflows) == 0

    def test_mtmt_mapping_loader_happy_path_multiple_elements(self):

        # GIVEN a mapping file with many trustzones
        # AND many components
        default_mapping_file = (custom_mtmt_multiple_mapping_file, open(custom_mtmt_multiple_mapping_file, 'r'), 'text/yaml')

        # WHEN the load method of the MTMTMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader(default_mapping_file, None)
        mtmt_mapping_file_loader.load()

        # THEN a MTMTMapping is returned with many trustzones, many components and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.trustzones) == 1
        assert len(mtmt_mapping.components) == 1
        assert len(mtmt_mapping.dataflows) == 0

    def test_mtmt_mapping_loader_empty_component(self):
        # GIVEN a mapping file with a trustzone
        # AND a single empty component
        # WHEN the load method of the MTMTMappingFileLoader is called
        # THEN MTMTMapping is returned with one trustzone, and empty components and without dataflows
        pass

    def test_mtmt_mapping_loader_empty_trustzone(self):
        # GIVEN a mapping file with a component
        # AND an empty trustzone
        # WHEN the load method of the MTMTMappingFileLoader is called
        # THEN MTMTMapping is returned with one component, an empty trustzone and without dataflows
        pass

    def test_mtmt_mapping_loader_empty_file(self):
        # GIVEN an empty default mapping file
        # WHEN the load method of the MTMTMappingFileLoader is called
        # THEN a MTMTMapping is returned with empty trustzones, components and without dataflows
        pass

    def test_mtmt_mapping_loader_more_not_mandatory_labels(self):
        # GIVEN a mapping file with some additional label
        # WHEN the load method of the MTMTMappingFileLoader is called
        # THEN a MTMTMapping is returned with a trustzone, a component and without dataflows
        # AND the additional label is ignored
        pass

    def test_mtmt_mapping_loader_without_mandatory_fields(self):
        # GIVEN a mapping file without a mandatory label ("id"/"label"/"type") or field value
        # WHEN the load method of the MTMTMappingFileLoader is called
        # THEN an error LoadingMappingFileError is raised
        pass
