from unittest.mock import patch, MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.connector.validate_connector_strategy import ValidateConnectorStrategy
from slp_visio.slp_visio.load.vsdx_parser import VsdxParser


class TestVsdxParser:
    @patch("slp_visio.slp_visio.load.strategies.connector.impl.validate_connector_by_connects.ValidateConnectorByConnects.is_connector")
    @pytest.mark.parametrize('impl1_result', [True, False])
    def test_create_connector_when_strategy_returns_value(self, mock_strategy_impl1, impl1_result):
        # GIVEN a visio connector shape
        shape = MagicMock(ID=1001)

        # AND a diagram connector is returned by the strategy
        mock_strategy_impl1.return_value = impl1_result

        # WHEN a connector is created
        result = VsdxParser._is_connector(shape)

        # THEN the strategy implementations are the expected
        assert ValidateConnectorStrategy.get_strategies().__len__() == 1
        # AND the strategies method implementations are called once
        mock_strategy_impl1.assert_called_once()
        # AND the result is the expected
        assert result == impl1_result


