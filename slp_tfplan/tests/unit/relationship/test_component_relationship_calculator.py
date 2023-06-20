from unittest.mock import Mock

import pytest

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipType, \
    ComponentRelationshipCalculator
from slp_tfplan.tests.util.builders import build_mocked_component, build_mocked_otm

_component_parent_0 = build_mocked_component({
    'component_name': 'component_parent_0',
    'tf_type': 'aws_type',
})

_component_child_0 = build_mocked_component({
    'component_name': 'component_a',
    'tf_type': 'aws_type',
    'parent_id': _component_parent_0.id,
    'parent_type': ParentType.COMPONENT
})

_component_parent_1 = build_mocked_component({
    'component_name': 'component_parent_1',
    'tf_type': 'aws_type'
})

_component_child_1 = build_mocked_component({
    'component_name': '_component_child_0',
    'tf_type': 'aws_type',
    'parent_id': _component_parent_1.id,
    'parent_type': ParentType.COMPONENT
})
_component_unrelated = build_mocked_component({
    'component_name': 'component_c',
    'tf_type': 'aws_type'
})

_component_parent_0.clones_ids = [_component_parent_1.id]
_component_parent_1.clones_ids = [_component_parent_0.id]
_component_child_0.clones_ids = [_component_child_1.id]
_component_child_1.clones_ids = [_component_child_0.id]

otm = build_mocked_otm([
    _component_parent_0, _component_child_0, _component_parent_1, _component_child_1, _component_unrelated
])


class TestComponentRelationshipCalculator:

    @pytest.mark.parametrize('component_from, component_to, component_relationship_type', [
        pytest.param(_component_child_0, _component_child_0, ComponentRelationshipType.SAME, id='SAME'),
        pytest.param(_component_parent_0, _component_child_0, ComponentRelationshipType.ANCESTOR, id='ANCESTOR'),
        pytest.param(_component_parent_1, _component_child_0, ComponentRelationshipType.ANCESTOR_OF_ANY_CLONE,
                     id='ANCESTOR_OF_ANY_CLONE'),
        pytest.param(_component_parent_0, _component_child_1, ComponentRelationshipType.ANCESTOR_OF_ANY_CLONE,
                     id='ANCESTOR_OF_ANY_CLONE (reverse)'),
        pytest.param(_component_child_1, _component_parent_1, ComponentRelationshipType.DESCENDANT, id='DESCENDANT'),
        pytest.param(_component_child_1, _component_parent_0, ComponentRelationshipType.DESCENDANT_OF_ANY_CLONE,
                     id='DESCENDANT_OF_ANY_CLONE'),
        pytest.param(_component_child_0, _component_parent_1, ComponentRelationshipType.DESCENDANT_OF_ANY_CLONE,
                     id='DESCENDANT_OF_ANY_CLONE (reverse)'),
        pytest.param(_component_child_1, _component_unrelated, ComponentRelationshipType.UNRELATED, id='UNRELATED'),
    ])
    def test_get_relationship(self, component_from: TFPlanComponent, component_to: TFPlanComponent,
                              component_relationship_type: ComponentRelationshipType):
        # GIVEN a component relationship calculator
        # WHEN getting the relationship between two components
        # THEN the relationship is as expected
        assert ComponentRelationshipCalculator(otm).get_relationship(component_from, component_to) \
               == component_relationship_type

    @pytest.mark.parametrize('relationship, are_related', [
        pytest.param(ComponentRelationshipType.SAME, True, id='SAME'),
        pytest.param(ComponentRelationshipType.ANCESTOR, True, id='ANCESTOR'),
        pytest.param(ComponentRelationshipType.ANCESTOR_OF_ANY_CLONE, True, id='ANCESTOR_OF_ANY_CLONE'),
        pytest.param(ComponentRelationshipType.DESCENDANT, True, id='DESCENDANT'),
        pytest.param(ComponentRelationshipType.DESCENDANT_OF_ANY_CLONE, True, id='DESCENDANT_OF_ANY_CLONE'),
        pytest.param(ComponentRelationshipType.UNRELATED, False, id='UNRELATED'),
    ])
    def test_are_related(self, relationship: ComponentRelationshipType, are_related: bool):
        # GIVEN a component relationship calculator
        # WHEN checking if two components are related
        # THEN the result is as expected
        component_relationship_calculator = ComponentRelationshipCalculator(otm)
        component_relationship_calculator.get_relationship = lambda x, y: relationship
        assert component_relationship_calculator.are_related(Mock(), Mock()) == are_related
