from shapely.geometry import Polygon
from vsdx import Shape

from startleft.diagram.representation.visio.visio_shape_representer import VisioShapeRepresenter

PLOT_TYPE = 0 #Circle
# PLOT_TYPE = 1  # Square


def get_shape_width(shape: Shape):
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)


def get_shape_height(shape: Shape):
    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


class SimpleComponentRepresenter(VisioShapeRepresenter):

    def build_representation(self, shape: Shape) -> Polygon:
        center_x = float(shape.cells['PinX'].value)
        center_y = float(shape.cells['PinY'].value)
        width = get_shape_width(shape)
        height = get_shape_height(shape)

        points = [(center_x - (width/2), center_y + (height/2)),
                  (center_x + (width/2), center_y + (height/2)),
                  (center_x + (width/2), center_y - (height/2)),
                  (center_x - (width/2), center_y - (height/2))]

        return Polygon(points)
