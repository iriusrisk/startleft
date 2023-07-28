from typing import List
from unittest.mock import MagicMock

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

    def test_none_catch_all_config(self):
        # GIVEN a mapping loader with none configuration
        mapping_loader = MagicMock(configuration={})
        lucid_parser = LucidParser(*(MagicMock(),) * 3, mapping_loader)

        # WHEN _get_component_mappings is called in LucidParser
        component_mappings = lucid_parser._get_component_mappings()

        # THEN none components are mapped
        assert len(component_mappings) == 0

    @pytest.mark.parametrize('shape_type', [
        pytest.param("AmazonEC22017", id='2017'),
        pytest.param("DatabaseAWS19", id='AWS19'),
        pytest.param("AWSCloudAWS2021", id='AWS2021$'),
        pytest.param("ACAccessControlBlock", id='AC.*Block'),
        pytest.param("AEAndroidPhoneBlock", id='AE.*Block'),
        pytest.param("AGSUserBlock", id='AGS.*Block'),
        pytest.param("AVMActiveDirectoryVMBlock", id='AVM.*Block'),
        pytest.param("AzureDatabaseforPostgreSQLServersAzure2019", id='Azure2019'),
        pytest.param("WebApplicationFirewallPoliciesWAFAzure2021", id='Azure2021$'),
    ])
    def test_catch_all_by_regex(self, shape_type):
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

