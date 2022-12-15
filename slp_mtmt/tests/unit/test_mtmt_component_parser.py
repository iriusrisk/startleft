from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.tests.resources import test_resource_paths

diagram_representation = DiagramRepresentation(id_='project-test-diagram',
                                               name='Project Test Diagram Representation',
                                               type_=str(RepresentationType.DIAGRAM.value),
                                               size={'width': 2000, 'height': 2000}
                                               )


class TestMTMTComponentParser:
    components_expected_added_for_filled_mapping_file = [
        {'id': '53245f54-0656-4ede-a393-357aeaa2e20f',
         'name': 'Accounting PostgreSQL',
         'parent': {'trustZone': '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'},
         'properties': {'Azure Postgres DB Firewall Settings': 'Select',
                        'Azure Postgres DB TLS Enforced': 'Select',
                        'Name': 'Accounting PostgreSQL',
                        'Out Of Scope': 'false'},
         'representations': [{'id': '53245f54-0656-4ede-a393-357aeaa2e20f-representation',
                              'name': 'Accounting PostgreSQL Representation',
                              'position': {'x': 231, 'y': 40},
                              'representation': 'project-test-diagram',
                             'size': {'height': 100, 'width': 100}}],
         'type': 'CD-MICROSOFT-AZURE-DB-POSTGRESQL'},
        {'id': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10',
         'name': 'Mobile Client',
         'parent': {'trustZone': 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'},
         'properties': {'Mobile Client Technologies': 'Android',
                        'Name': 'Mobile Client',
                        'Out Of Scope': 'false'},
         'representations': [{'id': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10-representation',
                              'name': 'Mobile Client Representation',
                              'position': {'x': 101, 'y': 104},
                              'representation': 'project-test-diagram',
                              'size': {'height': 100, 'width': 100}}],
         'type': 'android-device-client'},
        {'id': '5d15323e-3729-4694-87b1-181c90af5045',
         'name': 'Public API v2',
         'parent': {'trustZone': '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'},
         'properties': {'Hosting environment': 'Select',
                        'Identity Provider': 'Select',
                        'Name': 'Public API v2',
                        'Out Of Scope': 'false',
                        'Web API Technologies': 'Select'},
         'representations': [{'id': '5d15323e-3729-4694-87b1-181c90af5045-representation',
                              'name': 'Public API v2 Representation',
                              'position': {'x': 21, 'y': 101},
                              'representation': 'project-test-diagram',
                              'size': {'height': 100, 'width': 100}}],
         'type': 'web-service'},
        {'id': '91882aca-8249-49a7-96f0-164b68411b48',
         'name': 'Azure File Storage',
         'parent': {'trustZone': '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'},
         'properties': {'CORS Enabled': 'Select',
                        'HTTPS Enforced': 'Select',
                        'Name': 'Azure File Storage',
                        'Network Security': 'Select',
                        'Out Of Scope': 'false',
                        'Storage Type': 'Select'},
         'representations': [{'id': '91882aca-8249-49a7-96f0-164b68411b48-representation',
                              'name': 'Azure File Storage Representation',
                              'position': {'x': 230, 'y': 169},
                              'representation': 'project-test-diagram',
                              'size': {'height': 100, 'width': 100}}],
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
