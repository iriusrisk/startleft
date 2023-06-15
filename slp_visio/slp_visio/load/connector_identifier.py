from vsdx import Shape

from slp_visio.slp_visio.load.strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategy


class ConnectorIdentifier:

    @staticmethod
    def is_connector(shape: Shape) -> bool:
        for strategy in ConnectorIdentifierStrategy.get_strategies():
            if strategy.is_connector(shape):
                return True

        return False
