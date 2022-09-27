from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser
from slp_mtmt.tests.resources import test_resource_paths


class TestMTMTComponentParser:

    components_expected_added_for_filled_mapping_file = [
        {'id': '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f', 'name': 'Phone', 'type': 'android-device-client',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Phone', 'Out Of Scope': 'false', 'Mobile OS': 'Android'}},
        {'id': 'b61d6911-338d-46a8-9f39-8dcd24abfe91', 'name': 'Attacker', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Attacker', 'Out Of Scope': 'false', 'Threat Agent': 'Curious Attacker'}}
    ]

    def test_parse_with_empty_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the default default_mtmt_mapping_file
        with open(test_resource_paths.mtmt_empty_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_component_parser = MTMTComponentParser(mtmt.get_mtmt(), mtmt_mapping)
        components = mtmt_component_parser.parse()

        assert len(components) == 0

    def test_parse_with_filled_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the default default_mtmt_mapping_file
        with open(test_resource_paths.mtmt_mapping_filled_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_component_parser = MTMTComponentParser(mtmt.get_mtmt(), mtmt_mapping)
        components = mtmt_component_parser.parse()

        assert len(components) == 2

        for index in range(0, len(components) - 1):
            assert components[index].json() == self.components_expected_added_for_filled_mapping_file[index]
