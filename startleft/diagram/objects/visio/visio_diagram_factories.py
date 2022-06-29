from vsdx import Shape

from startleft.diagram.objects.diagram_factories import DiagramComponentFactory, DiagramConnectorFactory
from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '') if shape.master_shape else ''


class VisioComponentFactory(DiagramComponentFactory):

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        return DiagramComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            origin=origin,
            representation=representer.build_representation(shape))


class VisioConnectorFactory(DiagramConnectorFactory):

    def create_connector(self, shape) -> DiagramConnector:
        connected_shapes = shape.connects
        if connected_shapes[0].from_rel == 'BeginX':
            return DiagramConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return DiagramConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)
