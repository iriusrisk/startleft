from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.tests.util.builders import DEFAULT_TRUSTZONE


#######
# OTM #
#######

def assert_parents(components: [TFPlanComponent], relationships: dict = None):
    for component in components:
        assert_parent(component=component, parent_id=relationships.get(component.id))


def assert_parent(component: TFPlanComponent, parent_id: str = None):
    if parent_id:
        assert component.parent_type == ParentType.COMPONENT
        assert component.parent == parent_id
    else:
        assert component.parent_type == ParentType.TRUST_ZONE
        assert component.parent == DEFAULT_TRUSTZONE.id


##########
# TFPLAN #
##########
def assert_resource_values(properties: {}):
    assert properties['val1'] == 'value1'
    assert properties['val2'] == 'value2'
