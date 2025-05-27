from typing import List
from unittest.mock import MagicMock, patch

import pytest
from pytest import fixture

from slp_visio.slp_visio.parse.lucid_parser import LucidParser
from slp_visio.slp_visio.parse.visio_parser import VisioParser


def __get_shapes(shape_ids: List[str]):
    return lambda _: {key: MagicMock() for key in shape_ids}


def __get_lucid_parser_method(method_name):
    return f"{VisioParser.__module__}.{VisioParser.__name__}.{method_name}"


@fixture(autouse=True)
def mocked_trustzone_mappings():
    yield []


@fixture(autouse=True)
def mocked_component_mappings():
    yield []


@fixture(autouse=True)
def mock_get_trustzone_mappings(mocker, mocked_trustzone_mappings):
    mocker.patch(__get_lucid_parser_method('_get_trustzone_mappings'), __get_shapes(mocked_trustzone_mappings))


@fixture(autouse=True)
def mock_get_component_mappings(mocker, mocked_component_mappings):
    mocker.patch(__get_lucid_parser_method('_get_component_mappings'), __get_shapes(mocked_component_mappings))


def mock_diagram():
    components = []
    return MagicMock(components=components)


class TestLucidParser:

    @pytest.mark.parametrize('catch_all_config', [
        pytest.param({}, id='None configuration'),
        pytest.param({'catch_all': False}, id='Configured as boolean'),
        pytest.param({'catch_all': 'False'}, id='Configured as string Capital F'),
        pytest.param({'catch_all': 'false'}, id='Configured as string ')
    ])
    def test_none_catch_all_config(self, catch_all_config):
        # GIVEN a mapping loader with none configuration
        mapping_loader = MagicMock(configuration=catch_all_config)
        diagram = MagicMock(components=[MagicMock(id='1', type="AmazonEC22017")])
        lucid_parser = LucidParser(*(MagicMock(),) * 2, diagram, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN none components are mapped
        assert len(component_mappings) == 0

    @pytest.mark.parametrize('shape_type', [
        pytest.param("AmazonEC2", id='aws shape'),
        pytest.param("AzureCloud", id='azure shape'),
        pytest.param("Database", id='infrastructure shape'),
        pytest.param("GenericShape", id='generic shape'),
    ])
    def test_catch_all_applies_to_all_shapes(self, shape_type):
        # GIVEN a mapping loader with catch_all configuration
        mapping_loader = MagicMock(configuration={'catch_all': 'empty-component'})
        # AND a diagram with a shape of the given type
        diagram = MagicMock(components=[MagicMock(id='1', type=shape_type)])
        lucid_parser = LucidParser(*(MagicMock(),) * 2, diagram, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN one component is mapped
        assert len(component_mappings) == 1
        # AND shape_id 1 is mapped as catch all
        assert '1' in component_mappings
        assert component_mappings['1']['label'] == shape_type
        assert component_mappings['1']['type'] == 'empty-component'

    @pytest.mark.parametrize('mocked_trustzone_mappings,mocked_component_mappings', [
        pytest.param(['2'], ['3'], id='one trustzone and one component mapped')
    ])
    def test_skip_mapped_shapes(self, mocked_trustzone_mappings, mocked_component_mappings):
        # GIVEN a mapping loader with catch_all configuration
        mapping_loader = MagicMock(configuration={'catch_all': 'empty-component'})
        # AND a diagram with 3 shapes
        diagram = MagicMock(components=[MagicMock(id='1', type='AmazonEC22017'),
                                        MagicMock(id='2', type='trustzone'),
                                        MagicMock(id='3', type='component')])
        lucid_parser = LucidParser(*(MagicMock(),) * 2, diagram, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN two component is mapped
        assert len(component_mappings) == 2
        # AND shape_id 1 is mapped as catch all
        assert '1' in component_mappings
        assert component_mappings['1']['label'] == 'AmazonEC22017'
        assert component_mappings['1']['type'] == 'empty-component'
        # AND shape_id 3 is mapped by invoking the super method
        assert '3' in component_mappings
        assert isinstance(component_mappings['3'], MagicMock)

    @pytest.mark.parametrize('skip_config,expected', [
        pytest.param({'skip': ['AmazonEC22017', 'AmazonAPIGatewayAWS2021']}, [], id='with version'),
        pytest.param({'skip': ['AmazonEC2', 'AmazonAPIGateway']}, [], id='without version'),
        pytest.param({}, ['5', '19'], id='without skip'),
        pytest.param({'skip': ''}, ['5', '19'], id='empty skip'),
        pytest.param({'skip': ['amazonEC22017', 'amazonAPIGatewayAWS2021']}, ['5', '19'],
                     id='typo in skip with version'),
        pytest.param({'skip': ['amazonEC2', 'amazonAPIGatewayAWS']}, ['5', '19'], id='typo in skip without version')
    ])
    @patch.object(VisioParser, '_get_component_mappings', return_value={'5': {'label': 'AmazonEC2', 'type': 'ec2'},
                                                                        '19': {'label': 'AmazonAPIGatewayAWS2021',
                                                                               'type': 'empty-component'}})
    def test_get_component_mappings_skip_config(self, visio_get_component_mappings, skip_config, expected):
        """
        Test the skip config without catch all configuration.

        This test function checks the behavior of remove components present in skip configuration.

        """
        # GIVEN a mapping loader with skip configuration
        mapping_loader = MagicMock(configuration=skip_config)
        # AND the diagram with these components
        ec2 = MagicMock(id='5', type='AmazonEC22017')
        apigw = MagicMock(id='19', type='AmazonAPIGatewayAWS2021')
        diagram = MagicMock(components=[ec2, apigw])
        # AND the parser
        lucid_parser = LucidParser(*(MagicMock(),) * 2, diagram, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN the components mapped are as expected
        assert sorted(list(component_mappings.keys())) == sorted(expected)

    @pytest.mark.parametrize('skip_config, expected', [
        pytest.param({}, ['5', '14', '19', '23'], id='no skip'),
        pytest.param({'skip': ['AmazonEC2']}, ['14', '19', '23'], id='mapped+skip'),
        pytest.param({'skip': ['Azure Storage', 'AmazonAPIGatewayAWS2021'], 'catch-all': 'empty-component'},
                     ['5', '14'], id='catchall+skip'),
        pytest.param({'skip': ['AmazonEC2', 'Azure Storage', 'CorporateDataCenterContainer2017'],
                      'catch-all': 'empty-component'},
                     ['19'], id='mapped+catchall+skip'),
    ])
    @patch.object(VisioParser, '_get_component_mappings',
                  return_value={'5': {'label': 'AmazonEC2', 'type': 'ec2'}})
    @patch.object(LucidParser, '_LucidParser__get_catch_all_mappings',
                  return_value={'14': {'label': 'CorporateDataCenterContainer2017', 'type': 'empty-component'},
                                '19': {'label': 'AmazonAPIGatewayAWS2021', 'type': 'empty-component'},
                                '23': {'label': 'Azure Storage', 'type': 'azure-storage'}})
    def test_skip_config_with_catch_all_config(self, visio_get_component_mappings, lucid__get_catch_all_mappings,
                                               skip_config, expected):
        """
        Test the skip config with catch all configuration.

        This test function checks the behavior of remove components present in skip configuration, this also removes
        components mapped previously by catch all configuration.

        """
        # GIVEN a mapping loader with skip configuration
        mapping_loader = MagicMock(configuration=skip_config)
        # AND the diagram with these components
        ec2 = MagicMock(id='5', type='AmazonEC22017')
        datacenter = MagicMock(id='14', type='CorporateDataCenterContainer2017')
        apigw = MagicMock(id='19', type='AmazonAPIGatewayAWS2021')
        azure_storage = MagicMock(id='23', type='Azure Storage')
        diagram = MagicMock(components=[ec2, datacenter, apigw, azure_storage])
        # AND the parser
        lucid_parser = LucidParser(*(MagicMock(),) * 2, diagram, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN the components mapped are as expected
        assert sorted(list(component_mappings.keys())) == sorted(expected)
