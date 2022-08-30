from math import pi

from shapely.geometry import Polygon

from slp_visio.objects.diagram_objects import DiagramLimits
from slp_visio.representation.visio.zone.zone import Zone


def upper_left_representation(x_formula, y_formula, limits: DiagramLimits) -> Polygon:
    if x_formula(limits.x_floor) < limits.x_floor:
        return Polygon([(limits.x_floor, limits.y_top),
                        (limits.x_floor, y_formula(limits.x_floor)),
                        (x_formula(limits.y_top), limits.y_top)])
    else:
        return Polygon([(limits.x_floor, limits.y_floor),
                        (x_formula(limits.x_floor), limits.y_floor),
                        (x_formula(limits.y_top), limits.y_top),
                        (limits.x_floor, limits.y_top)])


def upper_right_representation(x_formula, y_formula, limits: DiagramLimits) -> Polygon:
    if y_formula(limits.x_top) > limits.y_top:
        return Polygon([(x_formula(limits.y_floor), limits.y_floor),
                        (limits.x_top, limits.y_floor),
                        (limits.x_top, limits.y_top),
                        (x_formula(limits.y_top), limits.y_top)])
    else:
        return Polygon([(x_formula(limits.y_top), limits.y_top),
                        (limits.x_top, limits.y_top),
                        (limits.x_top, y_formula(limits.y_top))])


def lower_left_representation(x_formula, y_formula, limits: DiagramLimits) -> Polygon:
    if y_formula(limits.x_floor) > limits.y_top:
        return Polygon([(limits.x_floor, limits.y_floor),
                        (x_formula(limits.y_floor), limits.y_floor),
                        (x_formula(limits.y_top), limits.y_top),
                        (limits.x_floor, limits.y_top)])
    else:
        return Polygon([
            (limits.x_floor, limits.x_floor),
            (limits.x_floor, y_formula(limits.x_floor)),
            (x_formula(limits.y_floor), limits.y_floor)])


def lower_right_representation(x_formula, y_formula, limits: DiagramLimits) -> Polygon:
    if y_formula(limits.x_top) > limits.y_top:
        return Polygon([(x_formula(limits.y_floor), limits.y_floor),
                        (limits.x_top, limits.y_floor),
                        (limits.x_top, limits.y_top),
                        (x_formula(limits.y_top), limits.y_top)])
    else:
        return Polygon([(x_formula(limits.y_floor), limits.y_floor),
                        (limits.x_top, limits.y_floor),
                        (limits.x_top, y_formula(limits.x_top))])


irregular_zones = [
    Zone('UPPER_LEFT',
         lambda angle: pi / 4 <= angle <= (3 / 4) * pi,
         upper_left_representation),
    Zone('UPPER_RIGHT',
         lambda angle: 0 <= angle <= pi / 4 or (7 / 4) * pi <= angle <= 2 * pi,
         upper_right_representation),
    Zone('LOWER_LEFT',
         lambda angle: (3 / 4) * pi <= angle <= (5 / 4) * pi,
         lower_left_representation),
    Zone('LOWER_RIGHT',
         lambda angle: (5 / 4) * pi <= angle <= (7 / 4) * pi,
         lower_right_representation)
]