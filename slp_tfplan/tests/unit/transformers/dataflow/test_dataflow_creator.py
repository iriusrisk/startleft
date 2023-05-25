import uuid
from typing import List
from unittest.mock import Mock

from pytest import mark, param, raises, fixture

from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator import DataflowCreator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy
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
    yield Mock(components=[Mock()] * 5, dataflows=[], mapped_resources_ids=[])


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

    def test_dataflows_appended(self, mocked_otm, mocked_graph):
        # GIVEN a mocked OTM with some fake components
        # AND a mocked graph

        # AND two strategies returning one dataflow per each
        dataflow_strategy_1_result = 'C1 -> C2'
        dataflow_strategy_2_result = 'C3 -> C4'
        strategies = mocked_strategies([[dataflow_strategy_1_result], [dataflow_strategy_2_result]])

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()

        # THEN the dataflows from both strategies are in the result OTM
        assert mocked_otm.dataflows == [dataflow_strategy_1_result] + [dataflow_strategy_2_result]

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

    def test_repeated_dataflows(self, mocked_otm, mocked_graph):
        # GIVEN a mocked OTM with some fake components
        # AND a mocked graph

        # AND two strategies returning the same dataflow
        same_dataflow = 'C1 -> C2'
        strategies = mocked_strategies([[same_dataflow], [same_dataflow]])

        # WHEN DataflowCreator::transform is called
        DataflowCreator(otm=mocked_otm, graph=mocked_graph, strategies=strategies).transform()

        # THEN the OTM contains the dataflow only once
        assert mocked_otm.dataflows == [same_dataflow]

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
