from math import pi

from shapely.geometry import Polygon


class QuadrantZoneCreator:

    def __init__(self, angle_clearance: float, diagram_limits: tuple):
        self.angle_clearance = angle_clearance
        self.x_limit = diagram_limits[0]
        self.y_limit = diagram_limits[1]

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
        return Polygon([(0, y), (0, self.y_limit), (self.x_limit, self.y_limit), (self.x_limit, y)])

    def __lower_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(0, 0), (0, y), (self.x_limit, y), (self.x_limit, 0)])

    def __left_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(0, 0), (0, self.y_limit), (x, self.y_limit), (x, 0)])

    def __right_quadrant(self, x: float, y: float) -> Polygon:
        return Polygon([(x, 0), (x, self.y_limit), (self.x_limit, self.y_limit), (self.x_limit, 0)])
