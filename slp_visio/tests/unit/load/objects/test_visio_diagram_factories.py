from typing import List, Union
from unittest.mock import Mock

import pytest
from pytest import fixture, mark, param

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioConnectorFactory
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy


def mocked_strategy(result: Union[DiagramConnector, None, Exception]):
    strategy = Mock()
    strategy.create_connector = Mock(side_effect=[result])
    return strategy


def mocked_strategies(results: List[Union[DiagramConnector, None, Exception]]):
    return list(map(mocked_strategy, results))


def mocked_connector(c_id: int = 1001, from_id: int = 1, to_id: int = 2):
    return Mock(id=c_id, from_id=from_id, to_id=to_id)


@fixture
def strategies():
    return []


@fixture(autouse=True)
def mock_get_strategies(mocker, strategies):
    return mocker.patch(
        'slp_visio.slp_visio.load.strategies.connector.create_connector_strategy.CreateConnectorStrategy.get_strategies',
        return_value=strategies)


class TestVisioConnectorFactory:

    def test_create_connector_when_strategy_returns_value(self, mock_get_strategies):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # AND only one strategy that returns a connector
        strategy = mocked_strategy(mocked_connector())
        mock_get_strategies.return_value = [strategy]

        # WHEN a connector is created
        result = VisioConnectorFactory().create_connector(shape)

        # THEN the strategy implementations are the expected
        assert CreateConnectorStrategy.get_strategies().__len__() == 1
        # AND the strategies method implementations are called once
        strategy.create_connector.assert_called_once()
        # AND the result is the expected
        assert result.id == 1001
        assert result.to_id == 2
        assert result.from_id == 1

    @mark.parametrize('strategies,_id,_from,_to,valid_strategy', [
        param(mocked_strategies(
            [mocked_connector(c_id=1001, from_id=1, to_id=2),
             mocked_connector(c_id=2002, from_id=2, to_id=1)]),
            1001, 1, 2, 0),
        param(mocked_strategies(
            [mocked_connector(c_id=1001, from_id=1, to_id=2),
             None]),
            1001, 1, 2, 0),
        param(mocked_strategies(
            [None,
             mocked_connector(c_id=2002, from_id=9, to_id=21)]),
            2002, 9, 21, 1),
        param(mocked_strategies(
            [None,
             None,
             mocked_connector(c_id=3003, from_id=5, to_id=7)]),
            3003, 5, 7, 2)
    ])
    def test_create_connector_when_some_strategy_return_value(self, strategies, _id, _from, _to, valid_strategy: int):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        result = VisioConnectorFactory().create_connector(shape)

        # THEN we call strategies until we find the first valid strategy
        for i in range(0, valid_strategy):
            strategies[i].create_connector.assert_called_once()
        for i in range(valid_strategy + 1, len(strategies)):
            strategies[i].create_connector.assert_not_called()
        # AND the result is the returned by the first strategy
        assert result.id == _id
        assert result.to_id == _to
        assert result.from_id == _from

    @mark.parametrize('strategies', [
        param(mocked_strategies([Exception("Some Error")]), id='one error'),
        param(mocked_strategies([Exception("Some Error"), Exception("Other Error")]), id='two errors'),
        param(mocked_strategies([Exception("Some Error"), mocked_connector()]), id='first error, second valid'),
    ])
    def test_create_connector_when_some_strategy_return_error(self, strategies):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        with pytest.raises(Exception) as error:
            VisioConnectorFactory().create_connector(shape)

        # THEN the strategy implementations are the expected
        assert CreateConnectorStrategy.get_strategies().__len__() == len(strategies)

        # AND the first strategy is called
        strategies[0].create_connector.assert_called_once()

        # AND the error is propagated
        assert error.value.args[0] == 'Some Error'

    @mark.parametrize('strategies', [
        param(mocked_strategies([None]), id='one strategy'),
        param(mocked_strategies([None, None]), id='two strategies')
    ])
    def test_create_connector_when_strategy_does_not_return_value(self, strategies):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        result = VisioConnectorFactory().create_connector(shape)

        # THEN the strategy implementations are the expected
        assert CreateConnectorStrategy.get_strategies().__len__() == len(strategies)
        # AND the strategies method implementations are called once
        strategies[0].create_connector.assert_called_once()
        # AND no result is returned
        assert not result
