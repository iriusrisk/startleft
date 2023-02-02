from typing import Optional

from shapely.geometry import Point
from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.representation.simple_component_representer import SimpleComponentRepresenter
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

    def __init__(self):
        self.tolerance = 0.09
        self.representer: SimpleComponentRepresenter() = SimpleComponentRepresenter()

    def create_connector(self, shape: Shape, components: [Shape]) -> Optional[DiagramConnector]:

        begin_line = Point(shape.begin_x, shape.begin_y)
        end_line = Point(shape.end_x, shape.end_y)
        if not begin_line or not end_line:
            return None

        origin = self.__match_component(begin_line, components)
        target = self.__match_component(end_line, components)

        if not origin or not target:
            return None

        return DiagramConnector(shape.ID, origin, target, name=shape.text)

    def __match_component(self, point, components):

        for component in components:
            polygon = self.representer.build_representation(component)
            distance = polygon.exterior.distance(point)
            if distance <= self.tolerance:
                return component.ID
