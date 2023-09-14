from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategyContainer
from slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_connects import CreateConnectorByConnects
from slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_line_coordinates import \
    CreateConnectorByLineCoordinates


class TestCreateConnectorStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateConnectorStrategy
        strategies = [x.cls for x in CreateConnectorStrategyContainer.visio_strategies.args]

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0] == CreateConnectorByConnects
        assert strategies[1] == CreateConnectorByLineCoordinates
