from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TfplanComponent
from slp_tfplan.tests.util.builders import DEFAULT_TRUSTZONE


#######
# OTM #
#######

def assert_parents(components: [TfplanComponent], relationships: dict = None):
    for component in components:
        assert_parent(component=component, parent_id=relationships.get(component.id))


def assert_parent(component: TfplanComponent, parent_id: str = None):
    if parent_id:
        assert component.parent_type == ParentType.COMPONENT
        assert component.parent == parent_id
    else:
        assert component.parent_type == ParentType.TRUST_ZONE
        assert component.parent == DEFAULT_TRUSTZONE.id


##########
# TFPLAN #
##########
def assert_common_properties(properties: {}):
    assert properties['resource_mode'] == 'managed'
    assert properties['resource_provider_name'] == 'registry.terraform.io/hashicorp/aws'
    assert properties['resource_schema_version'] == 0
    assert properties['val1'] == 'value1'
    assert properties['senval1'] == 'value1'


def assert_resource_id(resource: {}):
    assert resource['resource_id'] == resource['properties']['resource_address']
