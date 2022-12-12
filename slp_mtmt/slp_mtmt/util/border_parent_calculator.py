VALUE = 'Value'
LEFT = 'Left'
TOP = 'Top'
WIDTH = 'Width'
HEIGHT = 'Height'


class BorderParentCalculator:

    @staticmethod
    def is_parent(parent, child):
        try:
            return BorderParentCalculator.__is_inside(parent, child)
        except (ValueError, KeyError, TypeError):
            return False

    @staticmethod
    def __get_shape_value(shape):
        return shape.source[VALUE]

    @staticmethod
    def __is_inside(parent, child):
        parent_value = BorderParentCalculator.__get_shape_value(parent)
        child_value = BorderParentCalculator.__get_shape_value(child)

        parent_left = int(parent_value[LEFT])
        child_left = int(child_value[LEFT])
        if parent_left > child_left:
            return False

        parent_top: int = int(parent_value[TOP])
        child_top = int(child_value[TOP])
        if parent_top > child_top:
            return False

        parent_width = int(parent_value[WIDTH])
        child_width = int(child_value[WIDTH])
        parent_right = parent_left + parent_width
        child_right = child_left + child_width
        if parent_right < child_right:
            return False

        parent_height = int(parent_value[HEIGHT])
        child_height = int(child_value[HEIGHT])
        parent_bottom = parent_top + parent_height
        child_bottom = child_top + child_height
        if parent_bottom < child_bottom:
            return False

        if parent_bottom == child_bottom and \
                parent_right == child_right and \
                parent_top == child_top and \
                parent_left == child_left:
            return False

        return True



