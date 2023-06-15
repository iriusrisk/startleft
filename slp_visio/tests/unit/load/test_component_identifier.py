from typing import List, Union
from unittest.mock import MagicMock, Mock

import pytest
from pytest import fixture

from slp_visio.slp_visio.load.component_identifier import ComponentIdentifier


def mocked_strategy(result: Union[bool, Exception]):
    strategy = Mock()
    strategy.is_component = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List[Union[bool, Exception]]):
    return list(map(mocked_strategy, results))


@fixture
def strategies():
    return []


@fixture(autouse=True)
def mock_get_strategies(mocker, strategies):
    return mocker.patch(
        'slp_visio.slp_visio.load.strategies.component.component_identifier_strategy.ComponentIdentifierStrategy.get_strategies',
        return_value=strategies)


class TestComponentIdentifier:

    @pytest.mark.parametrize('strategies,valid_strategy,expected', [
        (mocked_strategies([True, True]), 0, True),
        (mocked_strategies([True, False]), 0, True),
        (mocked_strategies([False, True]), 1, True),
        (mocked_strategies([False, False]), 2, False),
        (mocked_strategies([True, False, False]), 0, True),
        (mocked_strategies([False, False, True]), 2, True),
        (mocked_strategies([False, False, False]), 3, False)
    ])
    def test_create_component_when_strategy_returns_value(self, strategies, valid_strategy: int, expected):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001)

        # WHEN we check if the shape is a component
        result = ComponentIdentifier.is_component(shape)

        # THEN we call strategies until we find the first valid strategy
        for i in range(0, valid_strategy):
            strategies[i].is_component.assert_called_once()
        for i in range(valid_strategy + 1, len(strategies)):
            strategies[i].create_component.assert_not_called()
        # AND the result is true if any strategy returns true
        assert result == expected
