from copy import deepcopy
from typing import List, Dict

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.map.tfplan_mapper import TFPlanMapper
from slp_tfplan.tests.util.builders import build_base_otm

BASE_OTM = build_base_otm()

DEFAULT_TRUSTZONE = {
    'id': 'b61d6911-338d-46a8-9f39-8dcd24abfe91',
    'name': 'Public Cloud',
    'type': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
}


def build_resource(tf_type: str) -> {}:
    return build_multiple_resources([tf_type])


def build_multiple_resources(resource_types: List[str]) -> {}:
    result = {'resource': []}
    for resource_type in resource_types:
        result['resource'].append({
            'resource_id': f'{resource_type}.foo',
            'resource_type': resource_type,
            'resource_name': 'foo'
        })
    return result


def build_mapping(otm_type: str, tf_type: str = None, tf_regex: str = None, configuration: {} = None) -> {}:
    config = {'otm_type': otm_type}
    if tf_type:
        config['tf_type'] = tf_type
    if tf_regex:
        config['tf_regex'] = tf_regex
    if configuration:
        config['configuration'] = configuration
    return build_multiple_mappings([config])


def build_multiple_mappings(components: List[Dict]) -> {}:
    result = {
        'default_trustzone': DEFAULT_TRUSTZONE,
        'components': []
    }

    for component in components:
        elem = {'otm_type': component['otm_type'],
                'tf_type': component.get('tf_type', {'$regex': component.get('tf_regex')})}
        if bool(component.get('configuration', None)):
            elem['configuration'] = component['configuration']

        result['components'].append(elem)

    return result


class TestTFPlanMapper:

    def test_mapping_by_type(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        resource = build_resource(tf_type)

        # AND a mapping by type to some OTM type
        otm_type = 'vpc'
        mapping = build_mapping(otm_type, tf_type=tf_type)

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is added to the OTM
        assert len(otm.components) == 1
        component = otm.components[0]

        # AND the resource is mapped to the right type
        assert component.type == otm_type

        # AND source type is in the tag and the _tf_type field
        assert component.tf_type == tf_type
        assert component.tags[0] == tf_type

        # AND the parent of the component is the default TrustZone
        assert component.parent == DEFAULT_TRUSTZONE['id']
        assert component.parent_type == ParentType.TRUST_ZONE

    def test_mapping_by_regex(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        resource = build_resource(tf_type)

        # AND a mapping by type to some OTM type for some regex
        otm_type = 'vpc'
        mapping = build_mapping(otm_type, tf_regex='^aws_*')

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is added to the OTM
        assert len(otm.components) == 1
        component = otm.components[0]

        # AND the resource is mapped to the right type
        assert component.type == otm_type

        # AND source type is in the tag and the _tf_type field
        assert component.tf_type == tf_type
        assert component.tags[0] == tf_type

        # AND the parent of the component is the default TrustZone
        assert component.parent == DEFAULT_TRUSTZONE['id']
        assert component.parent_type == ParentType.TRUST_ZONE

    def test_mapping_by_skip(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        resource = build_resource(tf_type)

        # AND a skip by type
        mapping = build_multiple_mappings([
            {'otm_type': 'to-skip', 'tf_type': tf_type},
            {'otm_type': 'to-skip', 'tf_type': tf_type, 'configuration': {'skip': True}}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN the component is skipped
        assert len(otm.components) == 0

    def test_mapping_by_catchall(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        otm_type = 'vpc'
        otm_empty = 'empty-component'
        resource = build_multiple_resources([tf_type, f"{tf_type}_catchall"])

        # AND a catchall by regex
        mapping = build_multiple_mappings([
            {'otm_type': otm_type, 'tf_type': tf_type},
            {'otm_type': otm_empty, 'tf_regex': '^aws_*', 'configuration': {'catchall': True}}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN two components are added to the OTM
        assert len(otm.components) == 2
        assert otm.components[0].type == otm_type
        assert otm.components[1].type == otm_empty

    def test_mapping_by_singleton_catchall(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        otm_type = 'vpc'
        otm_empty = 'empty-component'
        resource = build_multiple_resources([tf_type, f"{tf_type}_catchall", f"{tf_type}_catchall2"])

        # AND a catchall by regex marked as singleton
        mapping = build_multiple_mappings([
            {'otm_type': otm_type, 'tf_type': tf_type},
            {'otm_type': otm_empty, 'tf_regex': '^aws_*', 'configuration': {'singleton': True, 'catchall': True}}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN three components are added to the OTM
        assert len(otm.components) == 3
        assert otm.components[0].type == otm_type
        # AND component is marked as singleton
        assert otm.components[1].type == otm_empty
        assert otm.components[1].is_singleton
        # AND component is marked as singleton
        assert otm.components[2].type == otm_empty
        assert otm.components[2].is_singleton

    def test_mapping_by_type_skip_and_catchall(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        tf_skip = f'{tf_type}_skip'
        tf_catchall = f'{tf_type}_catchall'
        otm_type = 'vpc'
        otm_empty = 'empty-component'
        resource = build_multiple_resources([tf_type, tf_skip, tf_catchall])

        # AND a type, skip and catchall
        mapping = build_multiple_mappings([
            {'otm_type': otm_type, 'tf_type': tf_type},
            {'otm_type': otm_type, 'tf_type': tf_skip},
            {'otm_type': 'to-skip', 'tf_type': tf_skip, 'configuration': {'skip': True}},
            {'otm_type': otm_empty, 'tf_regex': '^aws_*', 'configuration': {'catchall': True}}])

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TFPlanMapper::map is invoked
        TFPlanMapper(otm, resource, mapping).map()

        # THEN two components are added to the OTM
        assert len(otm.components) == 2
        assert otm.components[0].type == otm_type
        assert otm.components[1].type == otm_empty

