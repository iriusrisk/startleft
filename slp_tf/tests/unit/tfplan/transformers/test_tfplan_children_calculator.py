from tfplan.transformers.tfplan_children_calculator import TfplanChildrenCalculator
from slp_tf.tests.unit.tfplan.otm_graph_util import build_component_id, build_mocked_otm, build_graph, \
    assert_parents

CHILD_TYPE = 'aws_ecs_task_definition'
PARENT_TYPE = 'aws_ecs_service'


class TestTfplanChildrenCalculator:

    def test_default_trustzone(self):
        # GIVEN an OTM dict with one component and a default trustZone
        component_name = 'child'
        component_type = CHILD_TYPE
        component_id = build_component_id(component_name, component_type)
        otm = build_mocked_otm({component_name: component_type})

        # AND a graph with no relationships for the component
        graph = build_graph([(component_id, None)])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 1

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {})

    def test_one_straight_path(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component_name = 'child'
        child_component_type = CHILD_TYPE
        child_component_id = build_component_id(child_component_name, child_component_type)

        parent_component_name = 'parent'
        parent_component_type = PARENT_TYPE
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type})

        # AND a graph with a straight relationship from the parent to the child
        graph = build_graph([
            (parent_component_id, child_component_id),
            (child_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_one_path_no_mapped_resources(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component_name = 'child'
        child_component_type = CHILD_TYPE
        child_component_id = build_component_id(child_component_name, child_component_type)

        parent_component_name = 'parent'
        parent_component_type = PARENT_TYPE
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type})

        # AND a graph with an indirect relationship from the parent to the child
        graph = build_graph([
            (parent_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', child_component_id),
            (child_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanChildrenCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})
