from random import shuffle

from pytest import mark

from otm.otm.entity.component import Component
from slp_tf.slp_tf.parse.mapping.tf_path_ids_calculator import TerraformPathIdsCalculator


class MockedComponentIdGenerator:

    def __init__(self, name, type, parent_id):
        self.name = name
        self.type = type
        self.parent_id = parent_id

    @staticmethod
    def from_component_source(component_source: {}, parent_id: str, component_name: str = ''):
        return MockedComponentIdGenerator(
            name=component_source['_key'],
            type=component_source['Type'],
            parent_id=parent_id)

    def generate_id(self):
        return f'{self.parent_id}.{self.type}-{self.name}'


def create_otm_component(component_data: {}) -> Component:
    return Component(**component_data)


def to_otm_components(components_data: []) -> [Component]:
    return [create_otm_component(data) for data in components_data]


def shuffle_components(components: [Component]) -> [Component]:
    shuffle(components)
    return components


TRUSTZONE_PARENT_COMPONENT = to_otm_components([
    {
        'name': 'grandparent_1',
        'component_type': 'vpc',
        'parent_type': "trustZone",
        'source': {
            'grandparent_1': {},
            'Type': 'aws_vpc',
            '_key': 'grandparent_1'
        },
        'parent': 'tz-1',
        'tags': [],
        'component_id': 'gp1'
    }
])

TRUSTZONE_PARENT_PATH_IDS = {'gp1': 'tz-1.aws_vpc-grandparent_1'}

THREE_LEVELS_TWO_LEAFS_COMPONENTS = to_otm_components([
    {
        'name': 'parent_1',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'parent_1': {},
            'Type': 'aws_subnet',
            '_key': 'parent_1'
        },
        'parent': 'gp1',
        'tags': [],
        'component_id': 'p1'
    }, {
        'name': 'grandparent_1',
        'component_type': 'vpc',
        'parent_type': "trustZone",
        'source': {
            'grandparent_1': {},
            'Type': 'aws_vpc',
            '_key': 'grandparent_1'
        },
        'parent': 'tz-1',
        'tags': [],
        'component_id': 'gp1'
    }, {
        'name': 'parent_2',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'parent_2': {},
            'Type': 'aws_subnet',
            '_key': 'parent_2'
        },
        'parent': 'gp1',
        'tags': [],
        'component_id': 'p2'
    }, {
        'name': 'child',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'child': {},
            'Type': 'aws_vpc_endpoint',
            '_key': 'child'
        },
        'parent': 'p1',
        'tags': [],
        'component_id': 'c1'
    }, {
        'name': 'child',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'child': {},
            'Type': 'aws_vpc_endpoint',
            '_key': 'child'
        },
        'parent': 'p2',
        'tags': [],
        'component_id': 'c2'
    }
])

THREE_LEVELS_TWO_LEAFS_PATH_IDS = {
    'c1': 'tz-1.aws_vpc-grandparent_1.aws_subnet-parent_1.aws_vpc_endpoint-child',
    'c2': 'tz-1.aws_vpc-grandparent_1.aws_subnet-parent_2.aws_vpc_endpoint-child',
    'p1': 'tz-1.aws_vpc-grandparent_1.aws_subnet-parent_1',
    'p2': 'tz-1.aws_vpc-grandparent_1.aws_subnet-parent_2',
    'gp1': 'tz-1.aws_vpc-grandparent_1',
}

TWO_TRUSTZONES_TWO_LEVELS_COMPONENTS = to_otm_components([
    {
        'name': 'grandparent_1',
        'component_type': 'empty-component',
        'parent_type': "trustZone",
        'source': {
            'grandparent_1': {},
            'Type': 'aws_subnet',
            '_key': 'grandparent_1'
        },
        'parent': 'tz1',
        'tags': [],
        'component_id': 'gp1'
    }, {
        'name': 'parent_1',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'parent_1': {},
            'Type': 'aws_subnet',
            '_key': 'parent_1'
        },
        'parent': 'gp1',
        'tags': [],
        'component_id': 'p1'
    }, {
        'name': 'grandparent_2',
        'component_type': 'empty-component',
        'parent_type': "trustZone",
        'source': {
            'grandparent_2': {},
            'Type': 'aws_subnet',
            '_key': 'grandparent_2'
        },
        'parent': 'tz2',
        'tags': [],
        'component_id': 'gp2'
    }, {
        'name': 'parent_2',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'parent_2': {},
            'Type': 'aws_subnet',
            '_key': 'parent_2'
        },
        'parent': 'gp2',
        'tags': [],
        'component_id': 'p2'
    }
])

TWO_TRUSTZONES_TWO_LEVELS_PATH_IDS = {
    'gp1': 'tz1.aws_subnet-grandparent_1',
    'p1': 'tz1.aws_subnet-grandparent_1.aws_subnet-parent_1',
    'gp2': 'tz2.aws_subnet-grandparent_2',
    'p2': 'tz2.aws_subnet-grandparent_2.aws_subnet-parent_2',
}

BROKEN_PATH_COMPONENTS = to_otm_components([
    {
        'name': 'grandparent',
        'component_type': 'empty-component',
        'parent_type': "trustZone",
        'source': {
            'grandparent': {},
            'Type': 'aws_subnet',
            '_key': 'grandparent'
        },
        'parent': 'tz1',
        'tags': [],
        'component_id': 'gp1'
    }, {
        'name': 'parent',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'parent': {},
            'Type': 'aws_subnet',
            '_key': 'parent'
        },
        'parent': 'unexisting_parent',
        'tags': [],
        'component_id': 'p1'
    }, {
        'name': 'child',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'child': {},
            'Type': 'aws_subnet',
            '_key': 'child'
        },
        'parent': 'p1',
        'tags': [],
        'component_id': 'c1'
    }
])

BROKEN_PATH_PATH_IDS = {
    'gp1': 'tz1.aws_subnet-grandparent'
}

UNEXISTING_PARENT_COMPONENT = to_otm_components([
    {
        'name': 'some_component',
        'component_type': 'empty-component',
        'parent_type': "component",
        'source': {
            'some_component': {},
            'Type': 'aws_subnet',
            '_key': 'some_component'
        },
        'parent': 'unexisting_parent',
        'tags': [],
        'component_id': 'c1'
    }
])


class TestTerraformPathIdsCalculator:

    @mark.parametrize('components, expected_path_ids',
                      [(THREE_LEVELS_TWO_LEAFS_COMPONENTS, THREE_LEVELS_TWO_LEAFS_PATH_IDS),
                       (TRUSTZONE_PARENT_COMPONENT, TRUSTZONE_PARENT_PATH_IDS),
                       (TWO_TRUSTZONES_TWO_LEVELS_COMPONENTS, TWO_TRUSTZONES_TWO_LEVELS_PATH_IDS)])
    def test_calculate_path_ids_happy_path(self, components, expected_path_ids):
        # GIVEN a list of well related components

        # WHEN calling calculate_path_ids
        path_ids = TerraformPathIdsCalculator(components, MockedComponentIdGenerator).calculate_path_ids()

        # THEN There are 22 resultant components
        assert len(path_ids) == len(expected_path_ids)

        # AND Each ID match its whole path
        assert path_ids == expected_path_ids

    @mark.parametrize('components',
                      [shuffle_components(THREE_LEVELS_TWO_LEAFS_COMPONENTS),
                       shuffle_components(THREE_LEVELS_TWO_LEAFS_COMPONENTS),
                       shuffle_components(THREE_LEVELS_TWO_LEAFS_COMPONENTS),
                       shuffle_components(THREE_LEVELS_TWO_LEAFS_COMPONENTS)])
    def test_different_orders(self, components: []):
        # GIVEN a list of hierarchical components in different orders

        # WHEN calling calculate_path_ids
        path_ids = TerraformPathIdsCalculator(components, MockedComponentIdGenerator).calculate_path_ids()

        # THEN There are 5 resultant components
        assert len(path_ids) == 5

        # AND Each ID match its whole path
        assert path_ids == THREE_LEVELS_TWO_LEAFS_PATH_IDS

    def test_nonexistent_parent(self):
        # GIVEN a component with a non-existing parent
        components = UNEXISTING_PARENT_COMPONENT

        # WHEN calling calculate_path_ids
        path_ids = TerraformPathIdsCalculator(components, MockedComponentIdGenerator).calculate_path_ids()

        # THEN no path_ids are returned
        assert len(path_ids) == 0

    def test_broken_path(self):
        # GIVEN a hierarchical component list with some broken path
        components = BROKEN_PATH_COMPONENTS

        # WHEN calling calculate_path_ids
        path_ids = TerraformPathIdsCalculator(components, MockedComponentIdGenerator).calculate_path_ids()

        # THEN only path ids are returned for components whose whole path can be calculated
        assert len(path_ids) == 1

        assert path_ids == BROKEN_PATH_PATH_IDS
