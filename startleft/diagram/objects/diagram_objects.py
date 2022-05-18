from shapely.geometry import Point, Polygon
from vsdx import Shape


class DiagramComponent:
    def __init__(self, id: str = None, name: str = None, type: str = None, parent=None, representation: Polygon = None):
        self.id = id
        self.name = name
        self.type = type
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
    components: [DiagramComponent]
    connectors: [DiagramConnector]

    def __init__(self, components: [DiagramComponent], connectors: [DiagramConnector]):
        self.components = components
        self.connectors = connectors
