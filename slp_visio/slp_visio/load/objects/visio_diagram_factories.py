from typing import Optional

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.util.visio import get_shape_text, get_master_shape_text


# if it has two shapes connected and is not pointing itself
def is_valid_connector(connected_shapes) -> bool:
    if len(connected_shapes) < 2:
        return False
    if connected_shapes[0].shape_id == connected_shapes[1].shape_id:
        return False
    return True


# if its master name includes 'Double Arrow' or has arrows defined in both ends
def is_bidirectional_connector(shape) -> bool:
    if shape.master_page.name is not None and 'Double Arrow' in shape.master_page.name:
        return True
    for arrow_value in [shape.cell_value(att) for att in ['BeginArrow', 'EndArrow']]:
        if arrow_value is None or not str(arrow_value).isnumeric() or arrow_value == '0':
            return False
    return True


def is_created_from(connector) -> bool:
    return connector.from_rel == 'BeginX'


def connector_has_arrow_in_origin(shape) -> bool:
    begin_arrow_value = shape.cell_value('BeginArrow')
    return begin_arrow_value is not None and str(begin_arrow_value).isnumeric() and begin_arrow_value != '0'


class VisioComponentFactory:

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=get_shape_text(shape),
            type=get_master_shape_text(shape),
            origin=origin,
            representation=representer.build_representation(shape))


class VisioConnectorFactory:

    def create_connector(self, shape) -> Optional[DiagramConnector]:
        connected_shapes = shape.connects
        if not is_valid_connector(connected_shapes):
            return None

        if is_bidirectional_connector(shape):
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id, True)

        has_arrow_in_origin = connector_has_arrow_in_origin(shape)

        if (not has_arrow_in_origin and is_created_from(connected_shapes[0])) \
                or (has_arrow_in_origin and is_created_from(connected_shapes[1])):
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)
