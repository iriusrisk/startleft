from math import tan, pi

from shapely.geometry import Polygon


def calc_slope_angle(angle):
    slot_angle = angle - pi / 4

    if slot_angle < 0:
        slot_angle = slot_angle + 2 * pi
    if slot_angle > pi:
        slot_angle = slot_angle - pi

    return slot_angle


def calc_slope(angle):
    return tan(calc_slope_angle(angle))


def y_formula(x_coordinate: float, slope: float, any_line_point: tuple):
    return x_coordinate * slope - any_line_point[0] * slope + any_line_point[1]


def x_formula(y_coordinate: float, slope: float, any_line_point: tuple):
    return any_line_point[0] + (y_coordinate - any_line_point[1]) / slope


def upper_left_orientation(angle) -> bool:
    return pi / 4 <= angle <= (3 / 4) * pi


def upper_right_orientation(x_value: float, y_value: float, angle: float) -> bool:
    return 0 <= angle <= pi / 4 or (7 / 4) * pi <= angle <= 2 * pi


def lower_left_orientation(x_value: float, y_value: float, angle: float) -> bool:
    return (3 / 4) * pi <= angle <= (5 / 4) * pi


def lower_right_orientation(x_value: float, y_value: float, angle: float) -> bool:
    return (5 / 4) * pi <= angle <= (7 / 4) * pi


class PolygonZoneCreator:

    def __init__(self, diagram_limits: tuple):
        self.x_limit = diagram_limits[0]
        self.y_limit = diagram_limits[1]
        self.orientations = {'UPPER_LEFT': {'condition': lambda angle: pi / 4 <= angle <= (3 / 4) * pi,
                                       'function': self.__create_upper_left_polygon},
                             'UPPER_RIGHT': {'condition': lambda angle: 0 <= angle <= pi / 4 or (7 / 4) * pi <= angle <= 2 * pi,
                                       'function': self.__create_upper_right_polygon},
                             'LOWER_LEFT': {'condition': lambda angle: (3 / 4) * pi <= angle <= (5 / 4) * pi,
                                       'function': self.__create_lower_left_polygon},
                             'LOWER_RIGHT': {'condition': lambda angle: (5 / 4) * pi <= angle <= (7 / 4) * pi,
                                       'function': self.__create_lower_right_polygon},
                             }

    def create_polygon(self, some_point: tuple, angle: float) -> Polygon:
        slope = calc_slope(angle)

        create_polygon_function = list(filter(lambda o: o['condition'](angle), self.orientations.values()))[0][
            'function']

        if create_polygon_function:
            return create_polygon_function(slope, some_point)

    def __create_upper_left_polygon(self, slope: float, some_point: tuple) -> Polygon:
        if x_formula(0, slope, some_point) < 0:
            return Polygon([(0, self.y_limit), (0, y_formula(0, slope, some_point)),
                            (x_formula(self.y_limit, slope, some_point), self.y_limit)])
        else:
            return Polygon([(0, 0), (x_formula(0, slope, some_point), 0),
                            (x_formula(self.y_limit, slope, some_point), self.y_limit), (0, self.y_limit)])

    def __create_upper_right_polygon(self, slope: float, some_point: tuple) -> Polygon:
        if y_formula(self.x_limit, slope, some_point) > self.y_limit:
            return Polygon([(x_formula(0, slope, some_point), 0), (self.x_limit, 0), (self.x_limit, self.y_limit), (x_formula(self.y_limit, slope, some_point), self.y_limit)])
        else:
            return Polygon([(x_formula(self.y_limit, slope, some_point), self.y_limit), (self.x_limit, self.y_limit), (self.x_limit, y_formula(self.y_limit, slope, some_point))])

    def __create_lower_left_polygon(self, slope: float, some_point: tuple) -> Polygon:
        if y_formula(0, slope, some_point) > self.y_limit:
            return Polygon([(0, 0), (x_formula(0, slope, some_point), 0), (x_formula(self.y_limit, slope, some_point), self.y_limit), (0, self.y_limit)])
        else:
            return Polygon([(0, 0), (0, y_formula(0, slope, some_point)), (x_formula(0, slope, some_point), 0)])

    def __create_lower_right_polygon(self, slope: float, some_point: tuple) -> Polygon:
        if y_formula(self.x_limit, slope, some_point) > self.y_limit:
            return Polygon([(x_formula(0, slope, some_point), 0), (self.x_limit, 0), (self.x_limit, self.y_limit), (x_formula(self.y_limit, slope, some_point), self.y_limit)])
        else:
            return Polygon([(x_formula(0, slope, some_point), 0), (self.x_limit, 0), (self.x_limit, y_formula(self.x_limit, slope, some_point))])

