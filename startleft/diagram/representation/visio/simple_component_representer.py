from shapely.geometry import Polygon, Point
from vsdx import Shape

from startleft.diagram.representation.visio.visio_shape_representer import VisioShapeRepresenter

# PLOT_TYPE = 0 #Circle
PLOT_TYPE = 1  # Square


def calculate_shape_dimension(shape: Shape):
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


class SimpleComponentRepresenter(VisioShapeRepresenter):

    def build_representation(self, shape: Shape) -> Polygon:
        return Point(float(shape.cells['PinX'].value), float(shape.cells['PinY'].value)) \
            .buffer(calculate_shape_dimension(shape), PLOT_TYPE)
