from slp_tf.slp_tf.tfplan.transformers.tfplan_parent_calculator import TfplanParentCalculator
from slp_tf.tests.unit.tfplan.otm_graph_util import build_component_id, build_mocked_otm, build_graph, \
    assert_parents

CHILD_TYPE = 'aws_instance'
PARENT_TYPES = ['aws_subnet', 'aws_vpc']


class TestTfplanParentCalculator:

    def test_default_trustzone(self):
        # GIVEN an OTM dict with one component and a default trustZone
        component_name = 'child'
        component_type = CHILD_TYPE
        component_id = build_component_id(component_name, component_type)
        otm = build_mocked_otm({component_name: component_type})

        # AND a graph with no relationships for the component
        graph = build_graph([(component_id, None)])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

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
        parent_component_type = PARENT_TYPES[0]
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type})

        # AND a graph with a straight relationship between the child and the parent
        graph = build_graph([
            (child_component_id, parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

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
        parent_component_type = PARENT_TYPES[0]
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type})

        # AND a graph with an indirect relationship between the child and the parent
        graph = build_graph([
            (child_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_two_paths_only_one_straight(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component_name = 'child'
        child_component_type = CHILD_TYPE
        child_component_id = build_component_id(child_component_name, child_component_type)

        parent_component_name = 'parent'
        parent_component_type = PARENT_TYPES[0]
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        grandparent_component_name = 'grandparent'
        grandparent_component_type = PARENT_TYPES[1]
        grandparent_component_id = build_component_id(grandparent_component_name, grandparent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type,
            grandparent_component_name: grandparent_component_type,
        })

        # AND a graph a two overlapped paths between a child and a parent
        graph = build_graph([
            (child_component_id, parent_component_id),
            (parent_component_id, grandparent_component_id),
            (grandparent_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 3

        # AND the parent are calculated according the relationships among components
        assert_parents(
            components=otm.components,
            relationships={child_component_id: parent_component_id, parent_component_id: grandparent_component_id})

    def test_two_straight_paths_different_lengths(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component_name = 'child'
        child_component_type = CHILD_TYPE
        child_component_id = build_component_id(child_component_name, child_component_type)

        parent_component_name = 'parent'
        parent_component_type = PARENT_TYPES[0]
        parent_component_id = build_component_id(parent_component_name, parent_component_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_name: parent_component_type,
        })

        # AND a graph a two overlapped paths between a child and a parent
        graph = build_graph([
            (child_component_id, parent_component_id),
            (child_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_two_straight_paths_same_lengths(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component_name = 'child'
        child_component_type = CHILD_TYPE
        child_component_id = build_component_id(child_component_name, child_component_type)

        parent_component_1_name = 'parent_1'
        parent_component_1_type = PARENT_TYPES[0]
        parent_component_1_id = build_component_id(parent_component_1_name, parent_component_1_type)

        parent_component_2_name = 'parent_2'
        parent_component_2_type = PARENT_TYPES[1]
        parent_component_2_id = build_component_id(parent_component_2_name, parent_component_2_type)

        otm = build_mocked_otm({
            child_component_name: child_component_type,
            parent_component_1_name: parent_component_1_type,
            parent_component_2_name: parent_component_2_type
        })

        # AND a graph a two paths from the same child to two parents
        graph = build_graph([
            (child_component_id, parent_component_1_id),
            (child_component_id, parent_component_2_id),
            (parent_component_1_id, None),
            (parent_component_2_id, None)
        ])

        # WHEN TfplanParentCalculator::calculate_parents is invoked
        TfplanParentCalculator(otm=otm, graph=graph).transform()

        # THEN the child component is duplicated
        assert len(otm.components) == 4

        # AND the parent are calculated according the relationships among components
        assert_parents(
            components=otm.components,
            relationships={
                f'{child_component_id}_0': parent_component_1_id,
                f'{child_component_id}_1': parent_component_2_id,
            })
