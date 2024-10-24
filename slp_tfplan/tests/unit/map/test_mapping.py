from typing import List
from unittest.mock import MagicMock

import pytest

from slp_base import MappingFileNotValidError
from slp_tfplan.slp_tfplan.map.mapping import Mapping, ComponentMapping, TrustZoneMapping, AttackSurface

TZ_TYPE_0_ID = '944a88f6-b08a-4eee-a501-4499b12d1956'
TZ_TYPE_1_ID = 'e7b84a79-66ea-4322-8d5e-5029ef7ea007'


def _create_trustzone(value: str, default: bool = False, trust_rating: int = None) -> dict:
    trustzone = {
        'type': f'type-{value}',
        'name': f'name-{value}'
    }
    if trustzone:
        trustzone['$default'] = default

    if trust_rating:
        trustzone['risk'] = {
            'trust_rating': trust_rating
        }

    return trustzone


def _create_component(value: str, singleton: bool = False, category: str = None) -> dict:
    component = {
        'label': f'{value}',
        'type': f'type-{value}'
    }
    if singleton:
        component['$singleton'] = singleton
    if category:
        component['$category'] = category
    return component


class TestComponentMapping:

    @pytest.mark.parametrize('component_id, singleton, category', [
        pytest.param(1, False, None, id='not singleton component'),
        pytest.param(2, True, None, id='singleton component'),
        pytest.param(3, False, 'Category', id='category component'),
    ])
    def test_component_mapping(self, component_id: str, singleton: bool, category: str):
        # GIVEN a component dictionary
        component_dict = _create_component(component_id, singleton, category)
        # WHEN loading the ComponentMapping
        component_mapping = ComponentMapping(component_dict)
        # THEN attributes are mapped correctly
        assert component_mapping.label == component_dict['label']
        assert component_mapping.type == component_dict['type']
        assert component_mapping.configuration.get('$singleton') == singleton
        assert component_mapping.configuration.get('$category') == category
        assert len(component_mapping.__str__())


class TestTrustZoneMapping:

    @pytest.mark.parametrize('tz_id, tz_type, default, trust_rating, trust_rating_class', [
        pytest.param(TZ_TYPE_0_ID, 0, False, None, type(None),
                     id='not default with not trust rating'),
        pytest.param(TZ_TYPE_1_ID, 1, True, None, type(None),
                     id='default with not trust rating'),
        pytest.param(TZ_TYPE_0_ID, 0, False, 10, int,
                     id='not default with trust rating'),
        pytest.param(TZ_TYPE_1_ID, 1, True, 10, int,
                     id='default with trust rating'),
    ])
    def test_trustzone_mapping(self, tz_id: str, tz_type: str, default: bool, trust_rating: int, trust_rating_class: type):
        # GIVEN a trustzone dictionary
        trustzone_dict = _create_trustzone(tz_type, default, trust_rating)
        # WHEN loading the ComponentMapping
        trustzone_mapping = TrustZoneMapping(trustzone_dict)
        # THEN attributes are mapped correctly
        assert trustzone_mapping.id == tz_id
        assert trustzone_mapping.type == trustzone_dict['type']
        assert trustzone_mapping.name == trustzone_dict['name']
        assert trustzone_mapping.trust_rating == trustzone_dict.get('risk', {}).get('trust_rating', None)
        assert trustzone_mapping.is_default == trustzone_dict.get('$default', False)
        assert isinstance(trustzone_mapping.trust_rating, trust_rating_class)
        assert len(trustzone_mapping.__str__())


class TestAttackSurface:

    @pytest.mark.parametrize('client, trustzone_id, trustzones, error_info_detail', [
        pytest.param(None, 'tz-1', [MagicMock(id='tz-1')], 'Attack Surface must contain a client', id='without client'),
        pytest.param('c', None, [MagicMock(id='tz-1')], 'Attack Surface must contain a valid TrustZone',
                     id='without trustzone id'),
        pytest.param('c', 'tz-1', None, 'Attack Surface must contain a valid TrustZone', id='without trustzones'),
        pytest.param('c', 'tz-1', [MagicMock(id='tz-0')], 'Attack Surface must contain a valid TrustZone',
                     id='without a valid trustzone id'),
    ])
    def test_validate(self, client: str, trustzone_id: str, trustzones: List[TrustZoneMapping], error_info_detail: str):
        # GIVEN an attack surface dictionary
        attack_surface_dict = {}
        if client:
            attack_surface_dict['client'] = client
        if trustzone_id:
            attack_surface_dict['trustzone'] = trustzone_id
        # WHEN loading the AttackSurface Object
        # THEN a MappingFileNotValidError error is raised
        with pytest.raises(MappingFileNotValidError) as error_info:
            AttackSurface(attack_surface_dict, trustzones)
        # AND error has the correct info
        assert error_info.value.title == 'Mapping file not valid'
        assert error_info.value.detail == error_info_detail

    def test_attack_surface_mapping(self):
        # GIVEN an attack surface dictionary
        attack_surface_dict = {
            'client': 'c',
            'trustzone': 'type-1'
        }
        # AND a list of trustzones
        trustzones = [MagicMock(type='type-0'), MagicMock(type='type-1')]
        # WHEN loading the AttackSurface Object
        attack_surface_mapping = AttackSurface(attack_surface_dict, trustzones)
        # THEN attributes are mapped correctly
        assert attack_surface_mapping.client == 'c'
        assert attack_surface_mapping.trustzone == trustzones[1]
        assert len(attack_surface_mapping.__str__())


class TestMapping:

    @pytest.mark.parametrize('mapping_dict, error_info_detail', [
        pytest.param({'components': [_create_component('1')]},
                     'Mapping file must contain at least one TrustZone', id='without trustzones'),
        pytest.param({'trustzones': [_create_trustzone('1')]},
                     'Mapping file must contain at least one Component', id='without components'),
        pytest.param({'trustzones': [_create_trustzone('1')], 'components': [_create_component('1')]},
                     'Mapping file must contain a default TrustZone', id='without default trustzone')
    ])
    def test_validate(self, mapping_dict, error_info_detail):
        # GIVEN a mapping dictionary
        # WHEN loading the Mapping Object
        # THEN a MappingFileNotValidError error is raised
        with pytest.raises(MappingFileNotValidError) as error_info:
            Mapping(mapping_dict)
        # AND error has the correct info
        assert error_info.value.title == 'Mapping file not valid'
        assert error_info.value.detail == error_info_detail

    def test_trustzones(self):
        # GIVEN a dict with two Trustzones
        mapping_dict = {
            'trustzones': [_create_trustzone('0', True), _create_trustzone('1')],
            'components': [_create_component('0')]
        }
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute trustzones returns the data correctly
        assert len(mapping.trustzones) == 2
        assert mapping.trustzones[0].id == TZ_TYPE_0_ID
        assert mapping.trustzones[1].id == TZ_TYPE_1_ID
        assert len(mapping.__str__())

    def test_components(self):
        # GIVEN a dict with two Components
        mapping_dict = {
            'trustzones': [_create_trustzone('0', True)],
            'components': [_create_component('0'), _create_component('1')]
        }
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute components returns the data correctly
        assert len(mapping.components) == 2
        assert mapping.components[0].label == '0'
        assert mapping.components[1].label == '1'
        assert len(mapping.__str__())

    @pytest.mark.parametrize('configuration, expected', [
        pytest.param(None, [], id='configuration none exists'),
        pytest.param({}, [], id='configuration is empty'),
        pytest.param({'skip': []}, [], id='skip is an empty array'),
        pytest.param({'skip': ['attr1']}, ['attr1'], id='skip is an empty array'),
    ])
    def test_skip(self, configuration, expected):
        # GIVEN a dict with Skip configuration
        mapping_dict = {
            'trustzones': [_create_trustzone('0', True)],
            'components': [_create_component('0')]
        }
        if configuration is not None:
            mapping_dict['configuration'] = configuration
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute label_to_skip returns the data correctly
        assert mapping.label_to_skip == expected
        assert len(mapping.__str__())

    @pytest.mark.parametrize('configuration, label, otm_type', [
        pytest.param({'catch_all': 'c'}, {'$regex': r'^aws_\w*$'}, 'c',
                     id='catch_all is informed')
    ])
    def test_catch_all(self, configuration, label, otm_type):
        # GIVEN a dict with Catchall configuration
        mapping_dict = {
            'trustzones': [_create_trustzone('0', True)],
            'configuration': configuration
        }
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute catchall returns the data correctly
        assert mapping.catch_all.label == label
        assert mapping.catch_all.type == otm_type
        assert len(mapping.__str__())

    @pytest.mark.parametrize('configuration, label, otm_type', [
        pytest.param(None, None, None, id='configuration none exists'),
        pytest.param({}, None, None, id='configuration is empty')
    ])
    def test_catch_all_not_exists(self, configuration, label, otm_type):
        # GIVEN a dict with Catchall configuration
        mapping_dict = {
            'trustzones': [_create_trustzone('0', True)],
            'components': [_create_component('0')]
        }
        if configuration is not None:
            mapping_dict['configuration'] = configuration
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute catchall returns the data correctly
        assert mapping.catch_all is None
        assert len(mapping.__str__())

    def test_attack_surface(self):
        # GIVEN a dict with attack surface configuration
        trustzone = _create_trustzone('0', True)
        mapping_dict = {
            'trustzones': [trustzone],
            'components': [_create_component('0')],
            'configuration': {
                'attack_surface': {
                    'client': 'c',
                    'trustzone': trustzone.get('type')
                }
            }
        }
        # WHEN loading the Mapping Object
        mapping = Mapping(mapping_dict)
        # THEN the attribute attack_surface returns the data correctly
        assert mapping.attack_surface.client == 'c'
        assert mapping.attack_surface.trustzone.type == trustzone.get('type')
        assert len(mapping.__str__())
