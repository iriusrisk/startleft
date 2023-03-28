from typing import List
from unittest.mock import Mock

import pytest
from pytest import fixture

from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourcesMatcher


def mocked_strategy(result):
    strategy = Mock()
    strategy.are_related = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List):
    return list(map(mocked_strategy, results))


@fixture
def strategies():
    return []


@fixture(autouse=True)
def mock_get_strategies(mocker, strategies):
    return mocker.patch(
        'slp_tfplan.slp_tfplan.matcher.resource_matcher.get_strategies',
        return_value=strategies)


class TestResourceMatcher:

    def test_no_strategies(self):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND no strategies
        no_strategies_group = Mock()

        # WHEN ObjectsMatcher::are_related is called
        result = ResourcesMatcher(no_strategies_group).are_related(object_1, object_2)

        # THEN we call strategies until we find the first valid strategy
        assert not result

    @pytest.mark.parametrize('strategies,valid_strategy,expected', [
        (mocked_strategies([True, True]), 0, True),
        (mocked_strategies([True, False]), 0, True),
        (mocked_strategies([False, True]), 1, True),
        (mocked_strategies([False, False]), -1, False),
        (mocked_strategies([True, False, False]), 0, True),
        (mocked_strategies([False, False, True]), 2, True),
        (mocked_strategies([False, False, False]), -1, False)
    ])
    def test_first_strategy_applied(self, strategies, valid_strategy, expected):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND a StrategyGroup with mocked strategies
        mocked_strategy_group = Mock()

        # WHEN ObjectsMatcher::are_related is called
        result = ResourcesMatcher(mocked_strategy_group).are_related(object_1, object_2)

        # THEN we call strategies until we find the first valid strategy
        for i in range(0, valid_strategy):
            strategies[i].are_related.assert_called_once()

        # AND the result is true if any strategy returns true
        assert result == expected

    # TODO def test_error_on_strategy(self):
