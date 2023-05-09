from slp_tfplan.slp_tfplan.transformers.children_calculator import ChildrenCalculator
from slp_tfplan.tests.util.asserts import assert_parents
from slp_tfplan.tests.util.builders import build_tfgraph, \
    build_mocked_tfplan_component, build_mocked_otm

CHILD_TYPE = 'aws_ecs_task_definition'
PARENT_TYPE = 'aws_ecs_service'


class TestChildrenCalculator:

    def test_default_trustzone(self):
        # GIVEN an OTM dict with one component and a default trustZone
        component_a = build_mocked_tfplan_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        component_id = component_a.id
        otm = build_mocked_otm([component_a])

        # AND a graph with no relationships for the component
        graph = build_tfgraph([(component_id, None)])

        # WHEN ChildrenCalculator::calculate_parents is invoked
        ChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 1

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {})

    def test_one_straight_path(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_tfplan_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_tfplan_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPE,
        })
        parent_component_id = parent_component.id

        otm = build_mocked_otm([child_component, parent_component])

        # AND a graph with a straight relationship from the parent to the child
        graph = build_tfgraph([
            (parent_component_id, child_component_id),
            (child_component_id, None)
        ])

        # WHEN ChildrenCalculator::calculate_parents is invoked
        ChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_one_path_no_mapped_resources(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_tfplan_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_tfplan_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPE,
        })
        parent_component_id = parent_component.id

        otm = build_mocked_otm([child_component, parent_component])

        # AND a graph with an indirect relationship from the parent to the child
        graph = build_tfgraph([
            (parent_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', child_component_id),
            (child_component_id, None)
        ])

        # WHEN ChildrenCalculator::calculate_parents is invoked
        ChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})
