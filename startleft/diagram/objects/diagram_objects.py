from enum import Enum

from shapely.geometry import Polygon

from startleft.diagram.diagram_type import DiagramType


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
               + 'parent_id: ' + self.name + '}'

    def __repr__(self) -> str:
        return '{id: ' + str(self.id) + ', ' \
               + 'name: ' + self.name + ', ' \
               + 'parent_id: ' + self.name + '}'


class DiagramConnector:
    def __init__(self, id, from_id, to_id):
        self.id = id
        self.from_id = from_id
        self.to_id = to_id

    def __str__(self) -> str:
        return super().__str__()


class Diagram:
    def __init__(self, diagram_type: DiagramType, components: [DiagramComponent], connectors: [DiagramConnector]):
        self.diagram_type = diagram_type
        self.components = components
        self.connectors = connectors
