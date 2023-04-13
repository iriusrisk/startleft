from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy
from slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_connects import CreateConnectorByConnects


class TestCreateConnectorStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateConnectorStrategy
        strategies = CreateConnectorStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 1

        # AND we have the expected implementations
        assert strategies[0].__class__ == CreateConnectorByConnects