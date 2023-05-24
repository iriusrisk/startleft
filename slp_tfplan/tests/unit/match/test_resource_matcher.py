from typing import List
from unittest.mock import Mock

from pytest import raises, mark, param

from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourceMatcher
from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy
from slp_tfplan.tests.util.builders import MockedException

ERROR_MESSAGE = 'Error matching resources'


def mocked_strategy(result) -> Mock:
    strategy = Mock()
    strategy.are_related = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List) -> List[Mock]:
    return list(map(mocked_strategy, results))


class TestResourceSMatcher:

    def test_no_strategies(self):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND no strategies
        strategies = []

        # WHEN ObjectsMatcher::are_related is called
        result = ResourceMatcher(strategies=strategies).are_related(object_1, object_2)

        # THEN we call strategies until we find the first valid strategy
        assert not result

    @mark.parametrize('strategies,valid_strategy,expected', [
        param(mocked_strategies([True, True]), 0, True, id='all true'),
        param(mocked_strategies([True, False]), 0, True, id='first true'),
        param(mocked_strategies([False, True]), 1, True, id='second true'),
        param(mocked_strategies([False, False]), -1, False, id='none true'),
        param(mocked_strategies([True, False, False]), 0, True, id='first true, three strategies'),
        param(mocked_strategies([False, False, True]), 2, True, id='last true, three strategies'),
        param(mocked_strategies([False, False, False]), -1, False, id='none true, three strategies')
    ])
    def test_first_strategy_applied(self, strategies: List[Mock], valid_strategy: int, expected: bool):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND some mocked strategies

        # WHEN ResourceSMatcher::are_related is called
        result = ResourceMatcher(strategies).are_related(object_1, object_2)

        # THEN we call strategies until we find the first valid strategy
        for i in range(0, valid_strategy):
            strategies[i].are_related.assert_called_once()

        # AND the result is true if any strategy returns true
        assert result == expected

    @mark.parametrize('strategies', [
        param(mocked_strategies([MockedException(ERROR_MESSAGE), True]), id='first error'),
        param(mocked_strategies([False, MockedException(ERROR_MESSAGE), True]), id='middle error'),
        param(mocked_strategies([False, MockedException(ERROR_MESSAGE)]), id='last error')
    ])
    def test_error_in_strategy(self, strategies: List[MatchStrategy]):
        # GIVEN two mocked objects
        object_1 = Mock()
        object_2 = Mock()

        # AND some strategies which return or not errors

        # WHEN ResourceSMatcher::are_related is called
        # THEN the error is propagated
        with raises(MockedException) as ex:
            ResourceMatcher(strategies).are_related(object_1, object_2)
            assert ex.value.message == ERROR_MESSAGE
