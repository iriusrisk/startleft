from typing import Optional, List

from dependency_injector.wiring import inject, Provide

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategyContainer
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy


class VisioComponentFactory:

    @inject
    def __init__(self, strategies: List[CreateComponentStrategy] = Provide[
        CreateComponentStrategyContainer.visio_strategies]):
        self.strategies = strategies

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        for strategy in self.strategies:
            component = strategy.create_component(shape, origin=origin, representer=representer)
            if component:
                return component


class VisioConnectorFactory:

    @staticmethod
    def create_connector(shape) -> Optional[DiagramConnector]:
        for strategy in CreateConnectorStrategy.get_strategies():
            connector = strategy.create_connector(shape)
            if connector:
                return connector
