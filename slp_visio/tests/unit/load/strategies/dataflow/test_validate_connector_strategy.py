from slp_visio.slp_visio.load.strategies.connector.impl.validate_connector_by_connects import \
    ValidateConnectorByConnects
from slp_visio.slp_visio.load.strategies.connector.validate_connector_strategy import ValidateConnectorStrategy


class TestValidateConnectorStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateConnectorStrategy
        strategies = ValidateConnectorStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 1

        # AND we have the expected implementations
        assert strategies[0].__class__ == ValidateConnectorByConnects