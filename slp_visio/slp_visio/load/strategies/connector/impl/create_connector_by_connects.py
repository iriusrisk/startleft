from typing import Optional

from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy, \
    CreateConnectorStrategyContainer


@register(CreateConnectorStrategyContainer.visio_strategies)
class CreateConnectorByConnects(CreateConnectorStrategy):
    """
    Strategy to create a connector from the shape connects
    """

    def create_connector(self, shape: Shape, components=None) -> Optional[DiagramConnector]:
        connected_shapes = shape.connects
        if not self.are_two_different_shapes(connected_shapes):
            return None

        if self.is_bidirectional_connector(shape):
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id, True)

        has_arrow_in_origin = self.connector_has_arrow_in_origin(shape)

        if (not has_arrow_in_origin and self.is_created_from(connected_shapes[0])) \
                or (has_arrow_in_origin and self.is_created_from(connected_shapes[1])):
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)

    # if it has two shapes connected and is not pointing itself
    @staticmethod
    def are_two_different_shapes(connected_shapes) -> bool:
        if len(connected_shapes) < 2:
            return False
        if connected_shapes[0].shape_id == connected_shapes[1].shape_id:
            return False
        return True

    # if its master name includes 'Double Arrow' or has arrows defined in both ends
    @staticmethod
    def is_bidirectional_connector(shape) -> bool:
        if shape.master_page.name is not None and 'Double Arrow' in shape.master_page.name:
            return True
        for arrow_value in [shape.cell_value(att) for att in ['BeginArrow', 'EndArrow']]:
            if arrow_value is None or not str(arrow_value).isnumeric() or arrow_value == '0':
                return False
        return True

    @staticmethod
    def connector_has_arrow_in_origin(shape) -> bool:
        begin_arrow_value = shape.cell_value('BeginArrow')
        return begin_arrow_value is not None and str(begin_arrow_value).isnumeric() and begin_arrow_value != '0'

    @staticmethod
    def is_created_from(connector) -> bool:
        return connector.from_rel == 'BeginX'
