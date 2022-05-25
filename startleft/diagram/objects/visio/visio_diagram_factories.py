from shapely.geometry import Point
from vsdx import Shape

from startleft.diagram.objects.diagram_factories import DiagramComponentFactory, DiagramConnectorFactory
from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector

# PLOT_TYPE = 0 #Circle
PLOT_TYPE = 1  #Square


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '') if shape.master_shape else ''


def calculate_shape_representation(shape: Shape):
    return Point(float(shape.cells['PinX'].value), float(shape.cells['PinY'].value)) \
        .buffer(calculate_shape_dimension(shape), PLOT_TYPE)


def calculate_shape_dimension(shape: Shape):
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


class VisioComponentFactory(DiagramComponentFactory):

    def create_component(self, shape) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            representation=calculate_shape_representation(shape))


class VisioConnectorFactory(DiagramConnectorFactory):

    def create_connector(self, shape) -> DiagramConnector:
        connected_shapes = shape.connects
        if connected_shapes[0].from_rel == 'BeginX':
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)
