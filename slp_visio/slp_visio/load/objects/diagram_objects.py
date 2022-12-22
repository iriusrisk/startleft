from enum import Enum

from shapely.geometry import Polygon

from slp_base import DiagramType


class DiagramComponentOrigin(Enum):
    SIMPLE_COMPONENT = 1
    BOUNDARY = 2


class DiagramComponent:
    def __init__(self,
                 id: str = None,
                 name: str = None,
                 type: str = None,
                 origin: DiagramComponentOrigin = None,
                 parent=None,
                 representation: Polygon = None):
        self.id = id
        self.name = name
        self.type = type
        self.origin = origin
        self.parent = parent
        self.representation = representation

    def get_component_category(self):
        return 'trustZone' if not self.parent else 'component'

    def __str__(self) -> str:
        return '{id: ' + str(self.id) + ', ' \
               + 'name: ' + self.name + ', ' \
               + 'parent_id: ' + str(self.parent.id if self.parent else None) + '}'

    def __repr__(self) -> str:
        return '{id: ' + str(self.id) + ', ' \
               + 'name: ' + self.name + ', ' \
               + 'parent_id: ' + str(self.parent.id if self.parent else None) + '}'


class DiagramConnector:
    def __init__(self, id, from_id, to_id, bidirectional=False, name=None):
        self.id = id
        self.from_id = from_id
        self.to_id = to_id
        self.bidirectional = bidirectional
        self.name = name

    def __str__(self) -> str:
        return super().__str__()


class DiagramLimits:

    def __init__(self, limits):
        self.x_floor = limits[0][0]
        self.y_floor = limits[0][1]
        self.x_top = limits[1][0]
        self.y_top = limits[1][1]

    def __str__(self) -> str:
        return f'({self.x_floor}, {self.y_floor}), ({self.x_top}, {self.y_top})'


class Diagram:
    def __init__(self,
                 diagram_type: DiagramType,
                 components: [DiagramComponent],
                 connectors: [DiagramConnector],
                 limits: DiagramLimits = None):
        self.diagram_type = diagram_type
        self.components = components
        self.connectors = connectors
        self.limits = limits
