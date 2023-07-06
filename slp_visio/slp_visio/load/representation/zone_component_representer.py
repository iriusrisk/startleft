from math import pi, tan

from shapely.geometry import Polygon
from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits
from slp_visio.slp_visio.load.representation.visio_shape_representer import VisioShapeRepresenter
from slp_visio.slp_visio.load.representation.zone.irregular_zones import irregular_zones
from slp_visio.slp_visio.load.representation.zone.regular_zones import regular_zones
from slp_visio.slp_visio.parse.shape_position_calculator import ShapePositionCalculator
from slp_visio.slp_visio.util.visio import get_normalized_angle


def calc_slope_angle(angle):
    slope_angle = angle - pi / 4

    if slope_angle < 0:
        slope_angle = slope_angle + 2 * pi
    if slope_angle > pi:
        slope_angle = slope_angle - pi

    return slope_angle


def calc_slope(angle):
    return tan(calc_slope_angle(angle))


def calc_y_formula(slope: float, any_line_point: tuple):
    return lambda x: x * slope - any_line_point[0] * slope + any_line_point[1]


def calc_x_formula(slope: float, any_line_point: tuple):
    return lambda y: y / slope + any_line_point[0] - (any_line_point[1] / slope)


def represent_quadrant(angle: float, some_point: tuple, limits: DiagramLimits):
    for zone in regular_zones:
        if zone.condition(angle):
            return zone.representation(some_point[0], some_point[1], limits)


def represent_irregular_zone(angle: float, some_point: tuple, limits: DiagramLimits):
    slope = calc_slope(angle)
    x_formula = calc_x_formula(slope, some_point)
    y_formula = calc_y_formula(slope, some_point)

    for zone in irregular_zones:
        if zone.condition(angle):
            return zone.representation(x_formula, y_formula, limits)


class ZoneComponentRepresenter(VisioShapeRepresenter):

    def __init__(self, diagram_limits: DiagramLimits):
        self.diagram_limits = diagram_limits

    def build_representation(self, shape: Shape) -> Polygon:
        angle = get_normalized_angle(shape)
        calculator = ShapePositionCalculator(shape)
        shape_center = calculator.get_absolute_center()

        return represent_quadrant(angle, shape_center, self.diagram_limits) or \
            represent_irregular_zone(angle, shape_center, self.diagram_limits)
