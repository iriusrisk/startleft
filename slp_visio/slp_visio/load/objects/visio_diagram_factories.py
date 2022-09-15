from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '') if shape.master_shape else ''


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


def connector_has_begin_arrow_defined(shape) -> bool:
    begin_arrow_value = shape.cell_value('BeginArrow')
    return begin_arrow_value is not None and str(begin_arrow_value).isnumeric() and begin_arrow_value != '0'


class VisioComponentFactory:

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            origin=origin,
            representation=representer.build_representation(shape))


class VisioConnectorFactory:

    def create_connector(self, shape) -> Optional[DiagramConnector]:
        connected_shapes = shape.connects
        if not is_valid_connector(connected_shapes):
            return None

        bidirectional = is_bidirectional_connector(shape)
        has_begin_arrow = connector_has_begin_arrow_defined(shape)

        if (connected_shapes[0].from_rel == 'BeginX' and (bidirectional or not has_begin_arrow)) \
                or (connected_shapes[1].from_rel == 'BeginX' and not bidirectional and has_begin_arrow):
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id, bidirectional)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id, bidirectional)
