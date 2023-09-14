from typing import Optional, List

from vsdx import Shape
from dependency_injector.wiring import inject, Provide

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy, \
    CreateConnectorStrategyContainer


class LucidConnectorFactory:

    @inject
    def __init__(self, strategies: List[CreateConnectorStrategy] = Provide[
        CreateConnectorStrategyContainer.visio_strategies]):
        self.strategies = strategies

    def create_connector(self, shape: Shape, components: [Shape]) -> Optional[DiagramConnector]:
        for strategy in self.strategies:
            connector = strategy.create_connector(shape, components=components)
            if connector:
                return connector
