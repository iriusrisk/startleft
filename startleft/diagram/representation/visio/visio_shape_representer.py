from abc import abstractmethod

from shapely.geometry import Polygon
from vsdx import Shape


class VisioShapeRepresenter:

    @abstractmethod
    def build_representation(self, shape: Shape) -> Polygon:
        pass

