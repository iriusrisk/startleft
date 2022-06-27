from vsdx import Shape

from startleft.diagram.objects.diagram_factories import DiagramComponentFactory, DiagramConnectorFactory
from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector, DiagramComponentOrigin
from startleft.diagram.representation.visio.boundary_component_representer import BoundaryComponentRepresenter
from startleft.diagram.representation.visio.simple_component_representer import SimpleComponentRepresenter


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '') if shape.master_shape else ''


class VisioComponentFactory(DiagramComponentFactory):

    def __init__(self):
        self.representers = {
            DiagramComponentOrigin.SIMPLE_COMPONENT: SimpleComponentRepresenter(),
            DiagramComponentOrigin.BOUNDARY: BoundaryComponentRepresenter()
        }

    def create_component(self, shape, origin) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            origin=origin,
            representation=self.representers[origin].build_representation(shape))

    def set_diagram_limits(self, limit_coordinates: tuple):
        self.representers[DiagramComponentOrigin.BOUNDARY].diagram_limits = limit_coordinates


class VisioConnectorFactory(DiagramConnectorFactory):

    def create_connector(self, shape) -> DiagramConnector:
        connected_shapes = shape.connects
        if connected_shapes[0].from_rel == 'BeginX':
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)
