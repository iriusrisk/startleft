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


def precalc_y_formula(slope: float, any_line_point: tuple):
    return lambda x: x * slope - any_line_point[0] * slope + any_line_point[1]


def precalc_x_formula(slope: float, any_line_point: tuple):
    return lambda y: y / slope + any_line_point[0] - (any_line_point[1] / slope)


class PolygonZoneCreator:

    def __init__(self, diagram_limits: tuple):
        self.x_floor = diagram_limits[0][0]
        self.y_floor = diagram_limits[0][1]
        self.x_top = diagram_limits[1][0]
        self.y_top = diagram_limits[1][1]

        self.orientations = {'UPPER_LEFT': {
                                    'condition': lambda angle: pi / 4 <= angle <= (3 / 4) * pi,
                                    'function': self.__create_upper_left_polygon},
                             'UPPER_RIGHT': {
                                    'condition': lambda angle: 0 <= angle <= pi / 4 or (7 / 4) * pi <= angle <= 2 * pi,
                                    'function': self.__create_upper_right_polygon},
                             'LOWER_LEFT': {
                                    'condition': lambda angle: (3 / 4) * pi <= angle <= (5 / 4) * pi,
                                    'function': self.__create_lower_left_polygon},
                             'LOWER_RIGHT': {
                                    'condition': lambda angle: (5 / 4) * pi <= angle <= (7 / 4) * pi,
                                    'function': self.__create_lower_right_polygon},
                             }

    def create_polygon(self, some_point: tuple, angle: float) -> Polygon:
        slope = calc_slope(angle)
        x_formula = precalc_x_formula(slope, some_point)
        y_formula = precalc_y_formula(slope, some_point)

        create_polygon_function = list(filter(
            lambda o: o['condition'](angle), self.orientations.values()))[0]['function']

        if create_polygon_function:
            return create_polygon_function(x_formula, y_formula)

    def __create_upper_left_polygon(self, x_formula, y_formula) -> Polygon:
        if x_formula(self.y_floor) < self.x_floor:
            return Polygon([(self.x_floor, self.y_top),
                            (self.x_floor, y_formula(self.x_floor)),
                            (x_formula(self.y_top), self.y_top)])
        else:
            return Polygon([(self.x_floor, self.y_floor),
                            (x_formula(self.x_floor), self.y_floor),
                            (x_formula(self.y_top), self.y_top),
                            (self.x_floor, self.y_top)])

    def __create_upper_right_polygon(self, x_formula, y_formula) -> Polygon:
        if y_formula(self.x_top) > self.y_top:
            return Polygon([(x_formula(self.y_floor), self.y_floor),
                            (self.x_top, self.y_floor),
                            (self.x_top, self.y_top),
                            (x_formula(self.y_top), self.y_top)])
        else:
            return Polygon([(x_formula(self.y_top), self.y_top),
                            (self.x_top, self.y_top),
                            (self.x_top, y_formula(self.y_top))])

    def __create_lower_left_polygon(self, x_formula, y_formula) -> Polygon:
        if y_formula(0) > self.y_top:
            return Polygon([(self.x_floor, self.y_floor),
                            (x_formula(self.y_floor), self.y_floor),
                            (x_formula(self.y_top), self.y_top),
                            (self.x_floor, self.y_top)])
        else:
            return Polygon([
                (self.x_floor, self.x_floor),
                (self.x_floor, y_formula(self.x_floor)),
                (x_formula(self.y_floor), self.y_floor)])

    def __create_lower_right_polygon(self, x_formula, y_formula) -> Polygon:
        if y_formula(self.x_top) > self.y_top:
            return Polygon([(x_formula(0), 0),
                            (self.x_top, 0),
                            (self.x_top, self.y_top),
                            (x_formula(self.y_top), self.y_top)])
        else:
            return Polygon([(x_formula(0), 0),
                            (self.x_top, 0),
                            (self.x_top, y_formula(self.x_top))])
