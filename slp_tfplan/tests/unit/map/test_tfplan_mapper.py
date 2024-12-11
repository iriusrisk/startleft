from copy import deepcopy
from typing import List, Dict
from unittest.mock import MagicMock

from pytest import mark, param

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.map.tfplan_mapper import TFPlanMapper
from slp_tfplan.tests.util.builders import build_base_otm

BASE_OTM = build_base_otm()

DEFAULT_TRUSTZONE = {
    'id': 'b61d6911-338d-46a8-9f39-8dcd24abfe91',
    'name': 'Public Cloud',
    'type': 'b61d6911-338d-46a8-9f39-8dcd24abfe91',
    'risk': {'trust_rating': 10},
    '$default': True
}


def build_resource(resource_type: str) -> {}:
    return build_multiple_resources([resource_type])


def build_multiple_resources(resource_types: List[str]) -> {}:
    result = {'resource': []}
    for resource_type in resource_types:
        result['resource'].append({
            'resource_id': f'{resource_type}.foo',
            'resource_type': resource_type,
            'resource_name': 'foo'
        })
    return result


def __mock_trustzone(trustzone: {}):
    return MagicMock(
        id=trustzone.get('id'),
        type=trustzone.get('type'),
        name=trustzone.get('name'),
        trust_rating=trustzone.get('risk', {}).get('trust_rating', None),
        is_default=trustzone.get('$default')
    )


def __mock_component(component: {}):
    return MagicMock(
        label=component.get('label'),
        type=component.get('type'),
        configuration={'$singleton': component.get('$singleton', False)}
    )


def mock_mapping(components_dict: List[Dict], skip=None, catch_all_type: str=None) -> {}:
    if skip is None:
        skip = []
    components_mock = []
    catch_all = None

    for component in components_dict:
        components_mock.append(__mock_component(component))

    if catch_all_type:
        catch_all = __mock_component({
                'label': {'$regex': r'^aws_\w*$'},
                'type': catch_all_type
        })

    return MagicMock(
        default_trustzone=__mock_trustzone(DEFAULT_TRUSTZONE),
        trustzones=[__mock_trustzone(DEFAULT_TRUSTZONE)],
        components=components_mock,
        label_to_skip=skip,
        catch_all=catch_all

    )


class TestTFPlanMapper:

    def test_mapping_by_type(self):
        # GIVEN a resource of some TF type
        resource_type = 'aws_vpc'
        resource = build_resource(resource_type)

        # AND a mapping by type to some OTM type
        otm_type = 'vpc'
        mapping = mock_mapping([{'type': otm_type, 'label': resource_type}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is added to the OTM
        assert len(otm.components) == 1
        component = otm.components[0]

        # AND the resource is mapped to the right type
        assert component.type == otm_type

        # AND source type is in the tag and the resource_type field
        assert component.tf_type == resource_type
        assert component.tags[0] == resource_type

        # AND the parent of the component is the default TrustZone
        assert component.parent == DEFAULT_TRUSTZONE['id']
        assert component.parent_type == ParentType.TRUST_ZONE

    @mark.parametrize('regex,resource_type', [
        param(r'^aws_\w*$','aws_vpc', id='aws_vpc'),
        param(r'^a+$','a'*255, id='long_string'),
        param(r'^(a+)+$','a'*255, id='redos_attack'),
    ])
    def test_mapping_by_regex(self,regex,resource_type:str):
        # GIVEN a resource of some TF type
        resource = build_resource(resource_type)

        # AND a mapping by type to some OTM type for some regex
        otm_type = 'vpc'
        mapping = mock_mapping([{'type': otm_type, 'label': {'$regex': regex}}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is added to the OTM
        assert len(otm.components) == 1
        component = otm.components[0]

        # AND the resource is mapped to the right type
        assert component.type == otm_type

        # AND source type is in the tag and the resource_type field
        assert component.tf_type == resource_type
        assert component.tags[0] == resource_type

        # AND the parent of the component is the default TrustZone
        assert component.parent == DEFAULT_TRUSTZONE['id']
        assert component.parent_type == ParentType.TRUST_ZONE

    def test_mapping_by_skip(self):
        # GIVEN a resource of some TF type
        resource_type = 'aws_vpc'
        resource = build_resource(resource_type)

        # AND a skip by type
        mapping = mock_mapping([{'type': 'to-skip', 'label': resource_type}], skip=[resource_type])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is skipped
        assert len(otm.components) == 0

    def test_mapping_by_catchall(self):
        # GIVEN a resource of some TF type
        resource_type = 'aws_vpc'
        otm_type = 'vpc'
        otm_empty = 'empty-component'
        resource = build_multiple_resources([resource_type, f"{resource_type}_catchall"])

        # AND a catchall by regex
        mapping = mock_mapping([{'type': otm_type, 'label': resource_type}], catch_all_type=otm_empty)

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN two components are added to the OTM
        assert len(otm.components) == 2
        assert otm.components[0].type == otm_type
        assert otm.components[1].type == otm_empty

    def test_mapping_by_type_skip_and_catchall(self):
        # GIVEN a resource of some TF type
        resource_type = 'aws_vpc'
        tf_skip = f'{resource_type}_skip'
        tf_catchall = f'{resource_type}_catchall'
        otm_type = 'vpc'
        otm_empty = 'empty-component'
        resource = build_multiple_resources([resource_type, tf_skip, tf_catchall])

        # AND a type, skip and catchall
        mapping = mock_mapping([
            {'type': otm_type, 'label': resource_type},
            {'type': otm_type, 'label': tf_skip}],
            skip=[tf_skip], catch_all_type=otm_empty)

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN two components are added to the OTM
        assert len(otm.components) == 2
        assert otm.components[0].type == otm_type
        assert otm.components[1].type == otm_empty
