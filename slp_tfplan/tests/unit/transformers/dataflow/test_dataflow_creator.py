from random import randint
from typing import List
from unittest.mock import Mock

from pytest import mark, fixture, param

from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator import DataflowCreator
from slp_tfplan.tests.util.builders import build_tfgraph

MOCKED_GRAPH = build_tfgraph([])


def mocked_strategy(result):
    strategy = Mock()
    strategy.create_dataflows = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List):
    return list(map(mocked_strategy, results))


@fixture
def strategies():
    return []


@fixture(autouse=True)
def mock_get_strategies(mocker, strategies):
    return mocker.patch(
        'slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator.get_strategies',
        return_value=strategies)


class TestDataflowCreator:
    def test_no_strategies(self):
        # GIVEN some mocked components
        components = [Mock()] * randint(1, 5)

        # AND an OTM with those components and no dataflows
        otm = Mock(components=components, dataflows=[], mapped_resources_ids=[])

        # AND a mocked graph
        graph = MOCKED_GRAPH

        # AND no strategies

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm, graph).transform()

        # THEN no dataflows were added
        assert not otm.dataflows

    # TODO Separate in two tests, number of dataflows and expected dataflows
    @mark.parametrize('strategies,expected_dataflows', [
        param(mocked_strategies([['C1 -> C2']]), 1, id='one strategy, one dataflow per strategy'),
        param(mocked_strategies([['C1 -> C2', 'C3 -> C4'], ['C5 -> C6', 'C7 -> C8']]),
              4,
              id='two strategies, two dataflows per strategy')])
    def test_all_strategies_applied(self, strategies, expected_dataflows):
        # GIVEN some mocked components
        components = [Mock()] * randint(1, 5)

        # AND an OTM with those components and no dataflows
        otm = Mock(components=components, dataflows=[], mapped_resources_ids=[])

        # AND a mocked graph
        graph = MOCKED_GRAPH

        # AND different combinations of strategies

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm, graph).transform()

        # THEN the expected dataflows are generated
        assert len(otm.dataflows) == expected_dataflows

# TODO def test_error_on_strategy(self):
