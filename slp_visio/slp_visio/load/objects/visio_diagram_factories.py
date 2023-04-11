from typing import Optional

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.strategies.dataflow.create_connector_strategy import CreateConnectorStrategy
from slp_visio.slp_visio.util.visio import get_shape_text, get_master_shape_text, normalize_label, get_unique_id_text


class VisioComponentFactory:

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=normalize_label(get_shape_text(shape)),
            type=normalize_label(get_master_shape_text(shape)),
            origin=origin,
            representation=representer.build_representation(shape),
            unique_id=get_unique_id_text(shape))


class VisioConnectorFactory:

    @staticmethod
    def create_connector(shape) -> Optional[DiagramConnector]:
        for strategy in CreateConnectorStrategy.get_strategies():
            connector = strategy.create_connector(shape)
            if connector:
                return connector
