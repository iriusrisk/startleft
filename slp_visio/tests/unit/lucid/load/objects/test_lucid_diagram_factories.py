from unittest.mock import Mock

import pytest
from pytest import mark, param

from slp_visio.slp_visio.lucid.load.objects.lucid_diagram_factories import LucidConnectorFactory
from slp_visio.tests.unit.load.objects.test_visio_diagram_factories import mocked_strategy, mocked_connector, \
    mocked_strategies


class TestLucidConnectorFactory:

    def test_create_connector_when_strategy_returns_value(self):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # AND only one strategy that returns a connector
        strategy = mocked_strategy(mocked_connector())

        # WHEN a connector is created
        result = LucidConnectorFactory(strategies=[strategy]).create_connector(shape, [])

        # THEN the strategies method implementations are called once
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
    def test_create_connector_when_some_strategy_return_value(self, strategies: list, _id, _from, _to,
                                                              valid_strategy: int):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        result = LucidConnectorFactory(strategies=strategies).create_connector(shape, [])

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
    def test_create_connector_when_some_strategy_return_error(self, strategies: list):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        with pytest.raises(Exception) as error:
            LucidConnectorFactory(strategies=strategies).create_connector(shape, [])

        # THEN  the first strategy is called
        strategies[0].create_connector.assert_called_once()

        # AND the error is propagated
        assert error.value.args[0] == 'Some Error'

    @mark.parametrize('strategies', [
        param(mocked_strategies([None]), id='one strategy'),
        param(mocked_strategies([None, None]), id='two strategies')
    ])
    def test_create_connector_when_strategy_does_not_return_value(self, strategies: list):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001)

        # WHEN a connector is created
        result = LucidConnectorFactory(strategies=strategies).create_connector(shape, [])

        # THEN the strategies method implementations are called once
        strategies[0].create_connector.assert_called_once()
        # AND no result is returned
        assert not result
