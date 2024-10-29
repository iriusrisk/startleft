from slp_tfplan.slp_tfplan.transformers.parent_calculator import ParentCalculator
from slp_tfplan.tests.util.asserts import assert_parents
from slp_tfplan.tests.util.builders import build_tfgraph, \
    build_mocked_otm, build_mocked_component

CHILD_TYPE = 'aws_instance'
PARENT_TYPES = ['aws_subnet', 'aws_vpc']


class TestParentCalculator:

    def test_default_trustzone(self):
        # GIVEN an OTM dict with one component and a default trustZone
        component_a = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        component_id = component_a.id

        otm = build_mocked_otm([component_a])

        # AND a graph with no relationships for the component
        graph = build_tfgraph([(component_id, None)])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 1

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {})

    def test_one_straight_path(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_id = parent_component.id

        otm = build_mocked_otm([child_component, parent_component])

        # AND a graph with a straight relationship between the child and the parent
        graph = build_tfgraph([
            (child_component_id, parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_one_path_no_mapped_resources(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_id = parent_component.id

        otm = build_mocked_otm([child_component, parent_component])

        # AND a graph with an indirect relationship between the child and the parent
        graph = build_tfgraph([
            (child_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_two_paths_only_one_straight(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_id = parent_component.id

        grandparent_component = build_mocked_component({
            'component_name': 'grandparent',
            'tf_type': PARENT_TYPES[1],
        })
        grandparent_component_id = grandparent_component.id

        otm = build_mocked_otm([child_component, parent_component, grandparent_component])

        # AND a graph a two overlapped paths between a child and a parent
        graph = build_tfgraph([
            (child_component_id, parent_component_id),
            (parent_component_id, grandparent_component_id),
            (grandparent_component_id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 3

        # AND the parent are calculated according the relationships among components
        assert_parents(
            components=otm.components,
            relationships={child_component_id: parent_component_id, parent_component_id: grandparent_component_id})

    def test_two_straight_paths_different_lengths(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component = build_mocked_component({
            'component_name': 'parent',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_id = parent_component.id

        otm = build_mocked_otm([child_component, parent_component])

        # AND a graph a two overlapped paths between a child and a parent
        graph = build_tfgraph([
            (child_component_id, parent_component_id),
            (child_component_id, 'non_mapped_component_id'),
            ('non_mapped_component_id', parent_component_id),
            (parent_component_id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN no extra components were added
        assert len(otm.components) == 2

        # AND the parent are calculated according the relationships among components
        assert_parents(otm.components, {child_component_id: parent_component_id})

    def test_two_straight_paths_same_length_to_subnets(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        parent_component_1 = build_mocked_component({
            'component_name': 'parent_1',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_1_id = parent_component_1.id

        parent_component_2 = build_mocked_component({
            'component_name': 'parent_2',
            'tf_type': PARENT_TYPES[0],
        })
        parent_component_2_id = parent_component_2.id

        otm = build_mocked_otm([child_component, parent_component_1, parent_component_2])

        # AND a graph a two paths from the same child to two parents
        graph = build_tfgraph([
            (child_component.id, parent_component_1.id),
            (child_component.id, parent_component_2.id),
            (parent_component_1.id, None),
            (parent_component_2.id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN the child component is duplicated
        assert len(otm.components) == 4

        # AND the parent are calculated according the relationships among components
        assert_parents(
            components=otm.components,
            relationships={
                f'{child_component_id}_0': parent_component_1_id,
                f'{child_component_id}_1': parent_component_2_id,
            })

    def test_two_straight_paths_same_length_to_subnet_and_network(self):
        # GIVEN an OTM dict with two components and a default trustZone
        child_component = build_mocked_component({
            'component_name': 'child',
            'tf_type': CHILD_TYPE,
        })
        child_component_id = child_component.id

        subnet = build_mocked_component({
            'component_name': 'subnet',
            'tf_type': PARENT_TYPES[0],
        })
        subnet_id = subnet.id

        network = build_mocked_component({
            'component_name': 'network',
            'tf_type': PARENT_TYPES[1],
        })
        network_id = network.id

        otm = build_mocked_otm([child_component, subnet, network])

        # AND a graph a two paths from the same child to two parents
        graph = build_tfgraph([
            (child_component.id, subnet.id),
            (child_component.id, network.id),
            (subnet.id, network.id),
            (network.id, None)
        ])

        # WHEN ParentCalculator::calculate_parents is invoked
        ParentCalculator(otm=otm, graph=graph).transform()

        # THEN the child component is not duplicated
        assert len(otm.components) == 3

        # AND the parent are calculated according the relationships among components
        assert_parents(
            components=otm.components,
            relationships={
                f'{child_component_id}': subnet_id,
                f'{subnet_id}': network_id,
            })
