import uuid
from typing import List
from unittest.mock import Mock

from pytest import mark, param, raises, fixture

from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator import DataflowCreator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import \
    DataflowCreationStrategy, create_dataflow
from slp_tfplan.tests.util.builders import build_tfgraph, MockedException

ERROR_MESSAGE = 'Error creating dataflows'


def mocked_strategy(result):
    strategy = Mock()
    strategy.create_dataflows = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List):
    return list(map(mocked_strategy, results))


def mocked_random_strategies(number_of_strategies, number_of_dataflows_per_strategy):
    return list(map(lambda _: mocked_strategy(
        [random_dataflow() for _ in range(number_of_dataflows_per_strategy)]), range(number_of_strategies)))


def random_dataflow() -> str:
    return str(uuid.uuid4())


@fixture(autouse=True)
def mocked_otm():
    components = [Mock(id=i, name=f'Component {i}') for i in range(0, 5)]
    yield Mock(components=components, dataflows=[], mapped_resources_ids=[])


@fixture(autouse=True)
def mocked_graph():
    yield build_tfgraph([])


class TestDataflowCreator:
    def test_no_strategies(self, mocked_otm, mocked_graph):
        # GIVEN a mocked OTM with some fake components
        # AND a mocked graph

        # AND no strategies
        strategies = []

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()

        # THEN no dataflows were added
        assert not mocked_otm.dataflows

    @mark.parametrize('strategy_results,expected_dataflows', [
        param([(0, 1, False)], [(0, 1, False)], id='simple dataflow'),
        param([(0, 1, False), (0, 1, False)], [(0, 1, False)], id='repeated dataflow'),
        param([(0, 1, False), (1, 0, False)], [(0, 1, False), (1, 0, False)], id='opposite dataflow'),
        param([(0, 1, True)], [(0, 1, True)], id='bidirectional dataflow'),
        param([(0, 1, True), (1, 0, True)], [(0, 1, True)], id='repeated bidirectional dataflow'),
        param([(0, 1, False), (1, 0, True)], [(0, 1, False), (1, 0, True)], id='single and bidirectional dataflow')
    ])
    def test_dataflows_created(self, mocked_otm, mocked_graph, strategy_results: List, expected_dataflows):
        # GIVEN a mocked OTM with some fake components
        components = mocked_otm.components

        # AND a mocked graph

        # AND some mocked strategies for each test parameter
        strategies = mocked_strategies(
            [[create_dataflow(components[sr[0]], components[sr[1]], bidirectional=sr[2])]
             for sr in strategy_results])

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()

        # THEN the dataflows are the expected
        assert len(mocked_otm.dataflows) == len(expected_dataflows)
        for i, dataflow in enumerate(mocked_otm.dataflows):
            # AND the source_node is right
            assert dataflow.source_node == expected_dataflows[i][0]

            # AND the destination node is right
            assert dataflow.destination_node == expected_dataflows[i][1]

            # AND the dataflow is bidirectional or not
            assert dataflow.bidirectional == expected_dataflows[i][2]

    def test_number_of_dataflows(self, mocked_otm, mocked_graph):
        # GIVEN a mocked OTM with some fake components
        # AND a mocked graph

        # AND a number of strategies returning another number of dataflows
        number_of_strategies = 4
        number_of_dataflows_per_strategy = 5
        strategies = mocked_random_strategies(number_of_strategies, number_of_dataflows_per_strategy)

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()

        # THEN all the dataflows from every strategy are included in the OTM
        assert len(mocked_otm.dataflows) == number_of_strategies * number_of_dataflows_per_strategy

    @mark.parametrize('strategies', [
        param(mocked_strategies([MockedException(ERROR_MESSAGE), []]), id='first error'),
        param(mocked_strategies([[], MockedException(ERROR_MESSAGE), []]), id='middle error'),
        param(mocked_strategies([[], MockedException(ERROR_MESSAGE)]), id='last error')
    ])
    def test_error_in_strategy(self, mocked_otm, mocked_graph, strategies: List[DataflowCreationStrategy]):
        # GIVEN a mocked OTM with some fake components
        # AND a mocked graph

        # AND some strategies which return or not errors

        # WHEN DataflowCreator::transform is called
        # THEN the error is propagated
        with raises(MockedException) as ex:
            DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()
            assert ex.value.message == ERROR_MESSAGE
