from math import radians, pi

from shapely.geometry import Polygon

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits
from slp_visio.slp_visio.load.representation.visio.zone.zone import Zone

ANGLE_CLEARANCE = radians(5)


def match_quadrant(shape_angle: float, quadrant_angle: float):
    return abs(shape_angle - quadrant_angle) <= ANGLE_CLEARANCE


def upper_quadrant_representation(x: float, y: float, limits: DiagramLimits) -> Polygon:
    return Polygon(
        [(limits.x_floor, y), (limits.x_floor, limits.y_top), (limits.x_top, limits.y_top), (limits.x_top, y)])


def lower_quadrant_representation(x: float, y: float, limits: DiagramLimits) -> Polygon:
    return Polygon(
        [(limits.x_floor, limits.y_floor), (limits.x_floor, y), (limits.x_top, y), (limits.x_top, limits.y_floor)])


def left_quadrant_representation(x: float, y: float, limits: DiagramLimits) -> Polygon:
    return Polygon(
        [(limits.x_floor, limits.y_floor), (limits.x_floor, limits.y_top), (x, limits.y_top), (x, limits.y_floor)])


def right_quadrant_representation(x: float, y: float, limits: DiagramLimits) -> Polygon:
    return Polygon(
        [(x, limits.y_floor), (x, limits.y_top), (limits.x_top, limits.y_top), (limits.x_top, limits.y_floor)])


regular_zones = [
    Zone('UPPER', lambda angle: match_quadrant(angle, pi / 4), upper_quadrant_representation),
    Zone('LOWER', lambda angle: match_quadrant(angle, (5 / 4) * pi), lower_quadrant_representation),
    Zone('LEFT', lambda angle: match_quadrant(angle, (3 / 4) * pi), left_quadrant_representation),
    Zone('RIGHT', lambda angle: match_quadrant(angle, (7 / 4) * pi), right_quadrant_representation)
]
