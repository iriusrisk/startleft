import copy
from typing import List
from unittest.mock import MagicMock, patch

from _pytest.mark import param
from pytest import mark

from otm.otm.entity.component import Component
from otm.otm.entity.trustzone import Trustzone
from slp_visio.slp_visio.parse.representation import trustzone_representation_calculator

__representation_id = 'representation_id'

__tz_without_representation = MagicMock()
__tz_without_representation.id = 'tz-id'
__tz_without_representation.name = 'tz-name'

__tz_representation = MagicMock()
__tz_representation.id = 'tz-id-representation'
__tz_representation.name = 'tz-name Representation'
__tz_representation.position = {'x': 70, 'y': 70}
__tz_representation.size = {'width': 210, 'height': 210}

__component_with_representation_1 = MagicMock(
    representations=[
        MagicMock(
            position={'x': 100, 'y': 100},
            size={'width': 50, 'height': 50}
        )
    ]
)

__component_with_representation_2 = MagicMock(
    representations=[
        MagicMock(
            position={'x': 200, 'y': 200},
            size={'width': 50, 'height': 50}
        )
    ]
)


@mark.parametrize('component, expected', [
    param(__component_with_representation_1, __component_with_representation_1.representations[0],
          id="Component has representation"),
    param(MagicMock(representations=[]), None, id="Component has representation length of zero"),
    param(MagicMock(), None, id="Component has not representation"),
])
def test_get_component_representation(component: Component, expected):
    # GIVEN the configured component
    # WHEN the method trustzone_representation_calculator::__get_component_representation is invoked
    representation = trustzone_representation_calculator.__get_component_representation(component)
    # THEN the representation is as expected
    assert representation == expected


@mark.parametrize('trustzone, components', [
    param(__tz_without_representation, [__component_with_representation_1, __component_with_representation_2],
          id="Calculate representation by 1 and 2"),
    param(__tz_without_representation, [__component_with_representation_2, __component_with_representation_1],
          id="Calculaste representation by 2 and 1"),
])
def test_calculate_tz_representation_by_components(trustzone: Trustzone, components: List[Component]):
    # GIVEN the configured trustzone with its related components
    # WHEN the method trustzone_representation_calculator::__calculate_tz_representation_by_components is invoked
    representation = trustzone_representation_calculator.__calculate_tz_representation_by_components \
        (__representation_id, trustzone, components)

    # THEN the representation is as expected
    assert representation.representation == __representation_id
    assert representation.id == __tz_representation.id
    assert representation.name == __tz_representation.name
    assert representation.position == __tz_representation.position
    assert representation.size == __tz_representation.size


def test_calculate_tz_representation_by_components_without_representation():
    # GIVEN the components without representations
    # WHEN the method trustzone_representation_calculator::__calculate_tz_representation_by_components is invoked
    representation = trustzone_representation_calculator.__calculate_tz_representation_by_components \
        (__representation_id, __tz_without_representation, [MagicMock(representations=[]), MagicMock()])
    # THEN no representation is calculated
    assert not representation


def test_calculate_relative_representation_by_tz():
    # GIVEN the configured components list
    components = [
        copy.deepcopy(__component_with_representation_1),
        copy.deepcopy(__component_with_representation_2)]
    # WHEN the method trustzone_representation_calculator::__calculate_relative_representation_by_tz is invoked
    trustzone_representation_calculator.__calculate_relative_representation_by_tz(
        MagicMock(representations=[__tz_representation]), components)

    # THEN the representations are as expected
    assert components[0].representations[0].position['x'] == 30
    assert components[0].representations[0].position['y'] == 30
    assert components[1].representations[0].position['x'] == 130
    assert components[1].representations[0].position['y'] == 130


root = 'slp_visio.slp_visio.parse.representation.trustzone_representation_calculator'


@patch(f'{root}.__calculate_tz_representation_by_components')
@patch(f'{root}.__calculate_relative_representation_by_tz')
def test_calculate_tz_representation(
        calculate_relative_representation_by_tz,
        calculate_tz_representation_by_components):
    # GIVEN the configured OTM
    representation_1 = MagicMock()
    representation_2 = MagicMock()
    component_1 = MagicMock()
    component_1.parent = __tz_without_representation.id
    otm = MagicMock()
    otm.trustzones = [__tz_without_representation, MagicMock(representations=[representation_2])]
    otm.components = [component_1]
    calculate_tz_representation_by_components.return_value = representation_1

    # WHEN the method trustzone_representation_calculator::calculate_tz_representation is invoked
    trustzone_representation_calculator.calculate_tz_representation(otm, __representation_id)

    # THEN the representations are as expected
    assert otm.trustzones[0].representations[0] == representation_1
    assert otm.trustzones[1].representations[0] == representation_2
    # AND the related methods are called once
    calculate_tz_representation_by_components.assert_called_once()
    calculate_relative_representation_by_tz.assert_called_once()
