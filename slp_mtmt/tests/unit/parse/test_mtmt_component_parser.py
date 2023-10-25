from unittest.mock import MagicMock

from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from sl_util.sl_util.file_utils import get_byte_data
from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import mtmt_default_mapping, \
    nested_trustzones_tm7, model_with_figures_without_name_file

diagram_representation = DiagramRepresentation(id_='project-test-diagram',
                                               name='Project Test Diagram Representation',
                                               type_=RepresentationType.DIAGRAM,
                                               size={'width': 2000, 'height': 2000}
                                               )


class TestMTMTComponentParser:
    components_expected_added_for_filled_mapping_file = [
        {'id': '53245f54-0656-4ede-a393-357aeaa2e20f',
         'name': 'Accounting PostgreSQL',
         'parent': {'trustZone': '24cdf4da-ac7f-4a35-bab0-29256d4169bf'},
         'attributes': {'Azure Postgres DB Firewall Settings': 'Select',
                        'Azure Postgres DB TLS Enforced': 'Select',
                        'Name': 'Accounting PostgreSQL',
                        'Out Of Scope': 'false'},
         'representations': [{'id': '53245f54-0656-4ede-a393-357aeaa2e20f-representation',
                              'name': 'Accounting PostgreSQL Representation',
                              'position': {'x': 231, 'y': 40},
                              'representation': 'project-test-diagram',
                              'size': {'height': 82, 'width': 82}}],
         'type': 'CD-MICROSOFT-AZURE-DB-POSTGRESQL'},
        {'id': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10',
         'name': 'Mobile Client',
         'parent': {'trustZone': '75605184-4ca0-43be-ba4c-5fa5ad15e367'},
         'attributes': {'Mobile Client Technologies': 'Android',
                        'Name': 'Mobile Client',
                        'Out Of Scope': 'false'},
         'representations': [{'id': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10-representation',
                              'name': 'Mobile Client Representation',
                              'position': {'x': 101, 'y': 104},
                              'representation': 'project-test-diagram',
                              'size': {'height': 82, 'width': 82}}],
         'type': 'android-device-client'},
        {'id': '5d15323e-3729-4694-87b1-181c90af5045',
         'name': 'Public API v2',
         'parent': {'trustZone': '24cdf4da-ac7f-4a35-bab0-29256d4169bf'},
         'attributes': {'Hosting environment': 'Select',
                        'Identity Provider': 'Select',
                        'Name': 'Public API v2',
                        'Out Of Scope': 'false',
                        'Web API Technologies': 'Select'},
         'representations': [{'id': '5d15323e-3729-4694-87b1-181c90af5045-representation',
                              'name': 'Public API v2 Representation',
                              'position': {'x': 21, 'y': 101},
                              'representation': 'project-test-diagram',
                              'size': {'height': 82, 'width': 82}}],
         'type': 'web-service'},
        {'id': '91882aca-8249-49a7-96f0-164b68411b48',
         'name': 'Azure File Storage',
         'parent': {'trustZone': '24cdf4da-ac7f-4a35-bab0-29256d4169bf'},
         'attributes': {'CORS Enabled': 'Select',
                        'HTTPS Enforced': 'Select',
                        'Name': 'Azure File Storage',
                        'Network Security': 'Select',
                        'Out Of Scope': 'false',
                        'Storage Type': 'Select'},
         'representations': [{'id': '91882aca-8249-49a7-96f0-164b68411b48-representation',
                              'name': 'Azure File Storage Representation',
                              'position': {'x': 230, 'y': 169},
                              'representation': 'project-test-diagram',
                              'size': {'height': 82, 'width': 82}}],
         'type': 'azure-storage'}
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
        mtmt_data = mtmt.get_mtmt()
        trustzone_parser = MTMTTrustzoneParser(mtmt_data, mtmt_mapping, diagram_representation.id)
        component_parser = MTMTComponentParser(mtmt_data, mtmt_mapping, trustzone_parser, diagram_representation.id)
        components = component_parser.parse()

        assert len(components) == 0

    def test_parse_with_filled_mapping_file(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_mvp, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the default default_mtmt_mapping_file
        with open(test_resource_paths.mapping_mtmt_mvp) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_data = mtmt.get_mtmt()
        trustzone_parser = MTMTTrustzoneParser(mtmt_data, mtmt_mapping, diagram_representation.id)
        component_parser = MTMTComponentParser(mtmt_data, mtmt_mapping, trustzone_parser, diagram_representation.id)
        components = component_parser.parse()

        assert len(components) == 4

        for index in range(0, len(components)):
            assert components[index].json() == self.components_expected_added_for_filled_mapping_file[index]

    def test_nested_trust_zones(self):
        # GIVEN the provider loader
        source_file = get_byte_data(nested_trustzones_tm7)
        mtmt: MTMTLoader = MTMTLoader(source_file)
        mtmt.load()

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(mtmt_default_mapping)

        # AND the mapping file loaded
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file])
        mtmt_mapping_file_loader.load()

        # WHEN we parse the components
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_data = mtmt.get_mtmt()
        trustzone_parser = MTMTTrustzoneParser(mtmt_data, mtmt_mapping, diagram_representation.id)
        component_parser = MTMTComponentParser(mtmt_data, mtmt_mapping, trustzone_parser, diagram_representation.id)
        components = component_parser.parse()

        # THEN we check the result is as expected
        assert len(components) == 4
        current = components[0]
        assert current.id == 'a38c22eb-fee8-4abd-b92c-457d6822ee86'
        assert current.parent == '26e6fdb8-013f-4d59-bb11-208eec4d6bc9'
        assert current.parent_type == 'trustZone'
        current = components[1]
        assert current.id == 'eef31b72-49b3-4d5f-9452-7ae178344c6b'
        assert current.parent == '351f4038-244d-4de5-bfa0-00c17f2a1fa2'
        assert current.parent_type == 'trustZone'
        current = components[2]
        assert current.id == '4820ec3a-9841-4baf-a38c-2fa596014274'
        assert current.parent == '9cbb5581-99cc-463b-a77a-c0dcae3b96d7'
        assert current.parent_type == 'trustZone'
        current = components[3]
        assert current.id == '9668ae2e-403f-4182-8c4c-d83948ffc31b'
        assert current.parent == '351f4038-244d-4de5-bfa0-00c17f2a1fa2'
        assert current.parent_type == 'trustZone'

    def test_model_components_without_name_file(self):
        # GIVEN the provider loader
        source_file = get_byte_data(model_with_figures_without_name_file)
        mtmt: MTMTLoader = MTMTLoader(source_file)
        mtmt.load()

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(mtmt_default_mapping)

        # AND the mapping file loaded
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file])
        mtmt_mapping_file_loader.load()

        # WHEN we parse the components
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        mtmt_data = mtmt.get_mtmt()
        component_parser = MTMTComponentParser(mtmt_data, mtmt_mapping, MagicMock(), diagram_representation.id)
        components = component_parser.parse()
        # THEN no component has None as name
        assert components[0].name == 'Generic External Interactor'
        assert components[1].name == 'Azure Traffic Manager'
        assert components[2].name == 'Database'
        assert components[3].name == 'Web Application'
