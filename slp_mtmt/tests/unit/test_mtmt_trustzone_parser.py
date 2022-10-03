from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.tests.resources import test_resource_paths


class TestMTMTTrustzoneParser:

    def test_parse_with_empty_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_mvp, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the mapping_file
        with open(test_resource_paths.mtmt_empty_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with no trustzones
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt.get_mtmt(), mtmt_mapping)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 0

    def test_parse_with_filled_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_mvp, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the mapping_file
        with open(test_resource_paths.mapping_mtmt_mvp) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with the expected trustzones
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt.get_mtmt(), mtmt_mapping)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 2
        trustzone = trustzones[0]
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        trustzone = trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'
