from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.tm7_to_json import Tm7ToJson
from slp_mtmt.tests.resources import test_resource_paths


class TestMTMTEntityBorder:
    border_attrs_expected_results = [
        {'id': '294a595a-174d-452c-b38d-9c434f7f5bac', 'name': 'My_MCU', 'type': 'StencilRectangle',
         'generic_type_id': 'c8bba3ee-9cdc-426f-89dd-0cea09ba72e8', 'is_component': True, 'is_trustzone': False,
         'stencil_name': 'MCU'},
        {'id': '436f7fa6-8555-4b73-9346-679874c650e7', 'name': 'SD card', 'type': 'StencilRectangle',
         'generic_type_id': 'c8bba3ee-9cdc-426f-89dd-0cea09ba72e8', 'is_component': True, 'is_trustzone': False,
         'stencil_name': 'Memory'},
        {'id': '241852d1-a5a7-4756-86d5-b400703b6614', 'name': 'Device Physical Boundary', 'type': 'BorderBoundary',
         'generic_type_id': '06836650-88ef-4421-a2d8-88cb8befbff0', 'is_component': False, 'is_trustzone': True,
         'stencil_name': 'Device Physical Boundary'},
        {'id': '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f', 'name': 'Phone', 'type': 'StencilRectangle',
         'generic_type_id': '8db306cc-f8f5-4c07-8be2-48e2a0af38aa', 'is_component': True, 'is_trustzone': False,
         'stencil_name': 'Phone'},
        {'id': '26418f1e-db19-41ad-9157-1ea2cebbaec6', 'name': 'SoC Boundary', 'type': 'BorderBoundary',
         'generic_type_id': '06836650-88ef-4421-a2d8-88cb8befbff0', 'is_component': False, 'is_trustzone': True,
         'stencil_name': 'SoC Boundary'},
        {'id': '8688c03a-1943-420c-8411-038d652220ca', 'name': 'Local Network Boundary', 'type': 'BorderBoundary',
         'generic_type_id': '06836650-88ef-4421-a2d8-88cb8befbff0', 'is_component': False, 'is_trustzone': True,
         'stencil_name': 'Local Network Boundary'},
        {'id': '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4', 'name': 'Server', 'type': 'StencilRectangle',
         'generic_type_id': '8db306cc-f8f5-4c07-8be2-48e2a0af38aa', 'is_component': True, 'is_trustzone': False,
         'stencil_name': 'Server'},
        {'id': '086f799f-e4f4-4c70-8f82-e1fd1212e22b', 'name': 'Company Internet Boundary', 'type': 'BorderBoundary',
         'generic_type_id': '06836650-88ef-4421-a2d8-88cb8befbff0', 'is_component': False, 'is_trustzone': True,
         'stencil_name': 'Company Internet Boundary'},
        {'id': 'ca3c7bc2-377f-471f-a45f-a78d511a4184', 'name': 'Attacker', 'type': 'StencilEllipse',
         'generic_type_id': 'dd163aaf-713b-46df-bc66-4ace6c033067', 'is_component': True, 'is_trustzone': False,
         'stencil_name': 'Attacker'}
    ]

    def test_mtmt_entity_border_attrs(self):
        # GIVEN the source MTMT data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()

        # AND the parser
        source = Tm7ToJson(xml).to_json()

        borders = []
        for border in source['ThreatModel']['DrawingSurfaceList']['DrawingSurfaceModel']['Borders'][
            'KeyValueOfguidanyType']:
            borders.append(MTMBorder(border))

        assert len(borders) == 9
        for index in range(0, len(borders) - 1):
            assert borders[index].id == self.border_attrs_expected_results[index]['id']
            assert borders[index].name == self.border_attrs_expected_results[index]['name']
            assert borders[index].type == self.border_attrs_expected_results[index]['type']
            assert borders[index].generic_type_id == self.border_attrs_expected_results[index]['generic_type_id']
            assert borders[index].is_component == self.border_attrs_expected_results[index]['is_component']
            assert borders[index].is_trustzone == self.border_attrs_expected_results[index]['is_trustzone']
            assert borders[index].stencil_name == self.border_attrs_expected_results[index]['stencil_name']

    border_properties_expected_results = [
        {'Name': 'My_MCU', 'Out Of Scope': 'false', 'OS': 'Bare Metal'},
        {'Name': 'SD card', 'Out Of Scope': 'false', 'ROM or RAM': 'ROM', 'removable': 'yes'},
        {'Name': 'Device Physical Boundary', 'Dataflow Order': '0'},
        {'Name': 'Phone', 'Out Of Scope': 'false', 'Mobile OS': 'Android'},
        {'Name': 'SoC Boundary', 'Dataflow Order': '0'},
        {'Name': 'Local Network Boundary', 'Dataflow Order': '0'},
        {'Name': 'Server', 'Out Of Scope': 'false'},
        {'Name': 'Company Internet Boundary', 'Dataflow Order': '0'},
        {'Name': 'Attacker', 'Out Of Scope': 'false', 'Threat Agent': 'Curious Attacker'}

    ]

    def test_mtmt_entity_border_properties(self):
        # GIVEN the source MTMT data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()

        # AND the parser
        source = Tm7ToJson(xml).to_json()

        borders = []
        for border in source['ThreatModel']['DrawingSurfaceList']['DrawingSurfaceModel']['Borders'][
            'KeyValueOfguidanyType']:
            borders.append(MTMBorder(border))

        for index in range(0, len(borders) - 1):
            assert borders[index].properties == self.border_properties_expected_results[index]

    def test_coordinates(self):
        # GIVEN the source MTMT border
        border_source = {
            'Key': '294a595a-174d-452c-b38d-9c434f7f5bac',
            'Value': {
                'Properties': {
                    'anyType': [
                        {'DisplayName': 'MCU'},
                        {'DisplayName': 'Name', 'Value': {'text': 'My_MCU'}}
                    ]
                },
                'Height': '100', 'Left': '145', 'Top': '57', 'Width': '200'
            },
            'attrib': {'Id': 'i2', 'type': 'StencilRectangle'}
        }

        # WHEN we instantiate the MTMTBorder
        border: MTMBorder = MTMBorder(border_source)

        # THEN we check the border
        assert border.properties == {'Name': 'My_MCU'}
        assert border.top == 57
        assert border.left == 145
        assert border.width == 200
        assert border.height == 100
        assert border.name == 'My_MCU'
        assert border.stencil_name == 'MCU'
        assert border.type == 'StencilRectangle'
        assert border.id == '294a595a-174d-452c-b38d-9c434f7f5bac'
        assert not border.is_trustzone
        assert border.is_component
