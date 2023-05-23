from typing import List
from unittest.mock import Mock

import pytest

from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourcesMatcher


def mocked_strategy(result):
    strategy = Mock()
    strategy.are_related = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List):
    return list(map(mocked_strategy, results))


class TestResourceMatcher:

    def test_no_strategies(self):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND no strategies
        strategies = []

        # WHEN ObjectsMatcher::are_related is called
        result = ResourcesMatcher(strategies=strategies).are_related(object_1, object_2)

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

        # AND some mocked strategies

        # WHEN ObjectsMatcher::are_related is called
        result = ResourcesMatcher(strategies).are_related(object_1, object_2)

        # THEN we call strategies until we find the first valid strategy
        for i in range(0, valid_strategy):
            strategies[i].are_related.assert_called_once()

        # AND the result is true if any strategy returns true
        assert result == expected

    # TODO def test_error_on_strategy(self):
