from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy


class LucidConnectorFactory:

    @staticmethod
    def create_connector(shape: Shape, components: [Shape]) -> Optional[DiagramConnector]:
        for strategy in CreateConnectorStrategy.get_strategies():
            connector = strategy.create_connector(shape, components=components)
            if connector:
                return connector
