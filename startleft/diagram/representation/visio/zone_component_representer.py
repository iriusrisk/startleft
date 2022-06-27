from math import radians, pi

from shapely.geometry import Polygon
from vsdx import Shape

from startleft.diagram.representation.visio.visio_shape_representer import VisioShapeRepresenter
from startleft.diagram.representation.visio.zone.polygon_zone_creator import PolygonZoneCreator
from startleft.diagram.representation.visio.zone.quadrant_zone_creator import QuadrantZoneCreator

DEFAULT_DIAGRAM_LIMITS = ((0, 0), (10, 10))
ANGLE_CLEARANCE = radians(5)


def get_shape_x(shape: Shape) -> float:
    return float(shape.cells['PinX'].value)


def get_shape_y(shape: Shape) -> float:
    return float(shape.cells['PinY'].value)


def get_shape_angle(shape: Shape) -> float:
    return float(shape.cells['Angle'].value)


def normalize_angle(angle: float) -> float:
    return angle + 2 * pi if angle < 0 else angle


class ZoneComponentRepresenter(VisioShapeRepresenter):

    def __init__(self, diagram_limits: tuple = None):
        self.diagram_limits = diagram_limits or DEFAULT_DIAGRAM_LIMITS
        self.quadrant_creator = QuadrantZoneCreator(ANGLE_CLEARANCE, self.diagram_limits)
        self.polygon_creator = PolygonZoneCreator(self.diagram_limits)

    def build_representation(self, shape: Shape) -> Polygon:
        shape_angle = normalize_angle(get_shape_angle(shape))
        x_value = get_shape_x(shape)
        y_value = get_shape_y(shape)

        return self.quadrant_creator.create_quadrant(x_value, y_value, shape_angle) or \
               self.polygon_creator.create_polygon((x_value, y_value), shape_angle)
