from copy import deepcopy

from otm.otm.entity.parent_type import ParentType
from slp_tf.slp_tf.tfplan.mapping.tfplan_mapper import TfplanMapper
from slp_tf.tests.unit.tfplan.otm_graph_util import build_base_otm

BASE_OTM = build_base_otm()

DEFAULT_TRUSTZONE = {
    'id': 'b61d6911-338d-46a8-9f39-8dcd24abfe91',
    'name': 'Public Cloud',
    'type': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
}


def build_resource(tf_type: str) -> {}:
    return {
        'resource': [
            {
                'resource_id': 'aws_vpc.foo',
                'resource_type': tf_type,
                'resource_name': 'foo'
            }
        ]
    }


def build_mapping(otm_type: str, tf_type: str = None, tf_regex: str = None) -> {}:
    return {
        'default_trustzone': DEFAULT_TRUSTZONE,
        'components': [
            {
                'otm_type': otm_type,
                'tf_type': tf_type if tf_type else {'$regex': tf_regex}
            }
        ]
    }


class TestTfplanMapper:

    def test_mapping_by_type(self):
        # GIVEN a resource of some TF type
        tf_type = 'aws_vpc'
        resource = build_resource(tf_type)

        # AND a mapping by type to some OTM type
        otm_type = 'vpc'
        mapping = build_mapping(otm_type, tf_type=tf_type)

        # AND a base otm dictionary
        otm = deepcopy(BASE_OTM)

        # WHEN TfplanMapper::map is invoked
        TfplanMapper(otm, resource, mapping).map()

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

        # WHEN TfplanMapper::map is invoked
        TfplanMapper(otm, resource, mapping).map()

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
