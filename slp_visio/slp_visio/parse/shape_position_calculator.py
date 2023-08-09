from vsdx.shapes import to_float, Shape


class ShapePositionCalculator:

    def __init__(self, shape: Shape):
        self.shape = shape
        self.max_levels = 12


    def get_absolute_center(self) -> {}:
        """
        The coordinates of a Visio shape are relatives:
        https://learn.microsoft.com/en-us/office/client-developer/visio/pinx-cell-shape-transform-section
        This method calculates the absolute coordinates of the center of the Shape
        """
        center = self._get_relative_center()
        parent: Shape = self.shape.parent
        level = 0
        while parent is not None and parent.ID is not None and level < self.max_levels:
            left = to_float(parent.center_x_y[0]) - (to_float(parent.width) / 2)
            top = to_float(parent.center_x_y[1]) - (to_float(parent.height) / 2)
            center = center[0] + left, center[1] + top
            parent = parent.parent
            level += 1
        return center

    def _get_relative_center(self):
        return tuple(map(float, self.shape.center_x_y))
