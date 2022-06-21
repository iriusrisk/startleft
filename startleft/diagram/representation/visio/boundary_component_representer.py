from shapely.geometry import Polygon
from vsdx import Shape

from startleft.diagram.representation.visio.visio_shape_representer import VisioShapeRepresenter


class BoundaryComponentRepresenter(VisioShapeRepresenter):

    def build_representation(self, shape: Shape) -> Polygon:
        pass
