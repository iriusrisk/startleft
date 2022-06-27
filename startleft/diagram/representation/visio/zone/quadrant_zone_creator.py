from math import pi

from shapely.geometry import Polygon


class QuadrantZoneCreator:

    def __init__(self, angle_clearance: float, diagram_limits: tuple):
        self.angle_clearance = angle_clearance
        self.x_floor = diagram_limits[0][0]
        self.y_floor = diagram_limits[0][1]
        self.x_top = diagram_limits[1][0]
        self.y_top = diagram_limits[1][1]

        self.quadrants = {
            'UPPER': {'angle': pi / 4, 'quadrant': self.__upper_quadrant},
            'LOWER': {'angle': (5 / 4) * pi, 'quadrant': self.__lower_quadrant},
            'LEFT': {'angle': (3 / 4) * pi, 'quadrant': self.__left_quadrant},
            'RIGHT': {'angle': (7 / 4) * pi, 'quadrant': self.__right_quadrant}
        }

    def create_quadrant(self, x_value: float, y_value: float, angle: float) -> Polygon:
        for quadrant in self.quadrants.values():
            if abs(angle - quadrant['angle']) <= self.angle_clearance:
                return quadrant['quadrant'](x_value, y_value)

    def __upper_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(self.x_floor, y), (self.x_floor, self.y_top), (self.x_top, self.y_top), (self.x_top, y)])

    def __lower_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(self.x_floor, self.y_floor), (self.x_floor, y), (self.x_top, y), (self.x_top, self.y_floor)])

    def __left_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(self.x_floor, self.y_floor), (self.x_floor, self.y_top), (x, self.y_top), (x, self.y_floor)])

    def __right_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(x, self.y_floor), (x, self.y_top), (self.x_top, self.y_top), (self.x_top, self.y_floor)])
