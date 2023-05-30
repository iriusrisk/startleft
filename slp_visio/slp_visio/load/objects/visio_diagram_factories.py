from typing import Optional

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy



class VisioComponentFactory:

    @staticmethod
    def create_component(shape, origin, representer) -> DiagramComponent:
        for strategy in CreateComponentStrategy.get_strategies():
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
