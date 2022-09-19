from startleft.processors.mtmt.mtmt_loader import MTMTLoader
from startleft.processors.mtmt.parse.mtmt_component_parser import MTMTComponentParser
from tests.resources import test_resource_paths
from tests.resources.test_resource_paths import mtmt_mapping_file


class TestMTMTComponentParser:
    components_expected_added = [
        {'id': '294a595a-174d-452c-b38d-9c434f7f5bac', 'name': 'My_MCU', 'type': 'StencilRectangle',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'My_MCU', 'Out Of Scope': 'false', 'OS': 'Bare Metal'}},
        {'id': '436f7fa6-8555-4b73-9346-679874c650e7', 'name': 'SD card', 'type': 'StencilRectangle',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'SD card', 'Out Of Scope': 'false', 'ROM or RAM': 'ROM', 'removable': 'yes'}},
        {'id': '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f', 'name': 'Phone', 'type': 'StencilRectangle',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Phone', 'Out Of Scope': 'false', 'Mobile OS': 'Android'}},
        {'id': '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4', 'name': 'Server', 'type': 'StencilRectangle',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Server', 'Out Of Scope': 'false'}},
        {'id': 'ca3c7bc2-377f-471f-a45f-a78d511a4184', 'name': 'Attacker', 'type': 'StencilEllipse',
         'parent': {'trustZone': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'},
         'properties': {'Name': 'Attacker', 'Out Of Scope': 'false', 'Threat Agent': 'Curious Attacker'}}
    ]

    def test_parse(self):
        # GIVEN the source MTMT data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()
        # AND the default default_mtmt_mapping_file
        mapping_file = mtmt_mapping_file

        mtmt_component_parser = MTMTComponentParser(mtmt.get_mtmt(), mapping_file)
        components = mtmt_component_parser.parse()

        for index in range(0, len(components) - 1):
            assert components[index].json() == self.components_expected_added[index]
