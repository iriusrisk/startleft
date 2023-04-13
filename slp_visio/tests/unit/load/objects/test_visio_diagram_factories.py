from unittest.mock import patch, MagicMock

from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioConnectorFactory
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy


class TestVisioConnectorFactory:

    @patch(
        "slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_connects.CreateConnectorByConnects.create_connector")
    def test_create_connector_when_strategy_returns_value(self, mock_strategy_impl1):
        # GIVEN a visio connector shape
        shape = MagicMock(ID=1001)

        # AND a diagram connector is returned by the strategy
        diagram_connector = MagicMock(id=1001, from_id=1, to_id=2)
        mock_strategy_impl1.return_value = diagram_connector

        # WHEN a connector is created
        result = VisioConnectorFactory().create_connector(shape)

        # THEN the strategy implementations are the expected
        assert CreateConnectorStrategy.get_strategies().__len__() == 1
        # AND the strategies method implementations are called once
        mock_strategy_impl1.assert_called_once()
        # AND the result is the expected
        assert result.id == 1001
        assert result.to_id == 2
        assert result.from_id == 1

    @patch(
        "slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_connects.CreateConnectorByConnects.create_connector")
    def test_create_connector_when_strategy_does_not_return_value(self, mock_strategy_impl1):
        # GIVEN a visio connector shape
        shape = MagicMock(ID=1001)

        # AND no diagram connector is returned by the strategy
        mock_strategy_impl1.return_value = None

        # WHEN a connector is created
        result = VisioConnectorFactory().create_connector(shape)

        # THEN the strategy implementations are the expected
        assert CreateConnectorStrategy.get_strategies().__len__() == 1
        # AND the strategies method implementations are called once
        mock_strategy_impl1.assert_called_once()
        # AND no result is returned
        assert not result
