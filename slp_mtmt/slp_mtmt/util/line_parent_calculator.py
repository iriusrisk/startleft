from shapely.geometry import Polygon, Point

from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.util.border_parent_calculator import LEFT, TOP, HEIGHT, WIDTH, VALUE
from slp_mtmt.slp_mtmt.util.math.line_utils import get_limit

limit_canvas = {'min': 0, 'max': 2000}


class LineParentCalculator:

    @staticmethod
    def is_parent(parent: MTMLine, child):
        try:
            return parent.is_trustzone and LineParentCalculator.__is_inside(parent, child)
        except (ValueError, KeyError, TypeError):
            return False

    @staticmethod
    def __is_inside(parent: MTMLine, child):

        child_value = child.source[VALUE]
        child_center_x = int(child_value[LEFT]) + int(child_value[WIDTH]) / 2
        child_center_y = int(child_value[TOP]) + int(child_value[HEIGHT]) / 2
        child_center = Point(child_center_x, child_center_y)

        triangle_a = parent.handle_x, parent.handle_y
        triangle_b = get_limit(parent.handle_x, parent.handle_y, parent.source_x, parent.source_y, limit_canvas['min'],
                               limit_canvas['max'])
        triangle_c = get_limit(parent.handle_x, parent.handle_y, parent.target_x, parent.target_y, limit_canvas['min'],
                               limit_canvas['max'])
        triangle = Polygon([triangle_a, triangle_b, triangle_c])

        return triangle.contains(child_center)
