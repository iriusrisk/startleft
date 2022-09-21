from startleft.processors.mtmt.mtmt_loader import MTMTLoader
from startleft.processors.mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from startleft.processors.mtmt.parse.mtmt_component_parser import MTMTComponentParser
from tests.resources import test_resource_paths
from tests.resources.test_resource_paths import mtmt_mapping_file, mtmt_mapping_filled_file


class TestMTMTComponentParser:
    components_expected_added_for_empty_mapping_file = [
        {'id': '294a595a-174d-452c-b38d-9c434f7f5bac', 'name': 'My_MCU', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'My_MCU', 'Out Of Scope': 'false', 'OS': 'Bare Metal'}},
        {'id': '436f7fa6-8555-4b73-9346-679874c650e7', 'name': 'SD card', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'SD card', 'Out Of Scope': 'false', 'ROM or RAM': 'ROM', 'removable': 'yes'}},
        {'id': '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f', 'name': 'Phone', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Phone', 'Out Of Scope': 'false', 'Mobile OS': 'Android'}},
        {'id': '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4', 'name': 'Server', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Server', 'Out Of Scope': 'false'}},
        {'id': 'ca3c7bc2-377f-471f-a45f-a78d511a4184', 'name': 'Attacker', 'type': 'empty-component',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Attacker', 'Out Of Scope': 'false', 'Threat Agent': 'Curious Attacker'}}
    ]

    components_expected_added_for_filled_mapping_file = [
        {'id': '294a595a-174d-452c-b38d-9c434f7f5bac', 'name': 'My_MCU', 'type': 'ec2',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'My_MCU', 'Out Of Scope': 'false', 'OS': 'Bare Metal'}},
        {'id': '436f7fa6-8555-4b73-9346-679874c650e7', 'name': 'SD card', 'type': 'ec2',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'SD card', 'Out Of Scope': 'false', 'ROM or RAM': 'ROM', 'removable': 'yes'}},
        {'id': '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f', 'name': 'Phone', 'type': 'ec2',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Phone', 'Out Of Scope': 'false', 'Mobile OS': 'Android'}},
        {'id': '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4', 'name': 'Server', 'type': 'ec2',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Server', 'Out Of Scope': 'false'}},
        {'id': 'ca3c7bc2-377f-471f-a45f-a78d511a4184', 'name': 'Attacker', 'type': 'ec2',
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
        with open(mtmt_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_component_parser = MTMTComponentParser(mtmt.get_mtmt(), mtmt_mapping)
        components = mtmt_component_parser.parse()

        for index in range(0, len(components) - 1):
            assert components[index].json() == self.components_expected_added_for_empty_mapping_file[index]

    def test_parse_with_filled_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the default default_mtmt_mapping_file
        with open(mtmt_mapping_filled_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_component_parser = MTMTComponentParser(mtmt.get_mtmt(), mtmt_mapping)
        components = mtmt_component_parser.parse()

        for index in range(0, len(components) - 1):
            assert components[index].json() == self.components_expected_added_for_filled_mapping_file[index]