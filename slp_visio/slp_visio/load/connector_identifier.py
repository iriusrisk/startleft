from functools import lru_cache
from typing import List

from dependency_injector.wiring import inject, Provide
from vsdx import Shape

from slp_visio.slp_visio.load.strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategy, \
    ConnectorIdentifierStrategyContainer


class ConnectorIdentifier:
    """
    Identifies if a Visio Shape is a representation of a data flow
    when we parse from Visio Shape to a DiagramComponent class
    """

    @inject
    def __init__(self, strategies: List[ConnectorIdentifierStrategy] = Provide[
        ConnectorIdentifierStrategyContainer.visio_strategies]):
        self.strategies = strategies

    @lru_cache(maxsize=None)
    def is_connector(self, shape: Shape) -> bool:
        for strategy in self.strategies:
            if strategy.is_connector(shape):
                return True

        return False
