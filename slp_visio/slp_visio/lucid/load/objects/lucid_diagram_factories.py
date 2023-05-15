from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy
from slp_visio.slp_visio.util.visio import get_shape_text, get_master_shape_text

LUCID_COMPONENT_PREFIX = 'com.lucidchart'


def is_lucid(shape: Shape):
    return shape.shape_name and shape.shape_name.startswith(LUCID_COMPONENT_PREFIX)


def get_lucid_component_type(shape: Shape):
    return shape.shape_name.replace(f'{LUCID_COMPONENT_PREFIX}.', '').replace(f'.{shape.ID}', '')


def get_component_type(shape):
    if is_lucid(shape):
        return get_lucid_component_type(shape)
    else:
        return get_master_shape_text(shape)


class LucidComponentFactory:

    @staticmethod
    def create_component(shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=get_shape_text(shape),
            type=get_component_type(shape),
            origin=origin,
            representation=representer.build_representation(shape))


class LucidConnectorFactory:

    @staticmethod
    def create_connector(shape: Shape, components: [Shape]) -> Optional[DiagramConnector]:
        for strategy in CreateConnectorStrategy.get_strategies():
            connector = strategy.create_connector(shape, components=components)
            if connector:
                return connector
