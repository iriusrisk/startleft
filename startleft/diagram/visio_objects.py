from shapely.geometry import Point
from vsdx import Shape

# PLOT_TYPE = 0 #Circle
PLOT_TYPE = 1  #Square


def calculate_shape_representation(shape: Shape):
    return Point(float(shape.cells['PinX'].value), float(shape.cells['PinY'].value)) \
        .buffer(calculate_shape_dimension(shape), PLOT_TYPE)


def calculate_shape_dimension(shape: Shape):
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


def get_component_type_from_master(shape: Shape):
    return shape.master_shape.text.replace('\n', '')


class VisioComponent:
    def __init__(self, id=None, name=None, type=None, parent=None, representation=None):
        self.id = id
        self.name = name
        self.type = type
        self.parent = parent
        self.representation = representation

    @staticmethod
    def from_shape(shape: Shape):
        return VisioComponent(
            id=shape.ID,
            name=shape.text.replace('\n', ''),
            type=get_component_type_from_master(shape),
            representation=calculate_shape_representation(shape))

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


class VisioConnector:
    def __init__(self, id, from_id, to_id):
        self.id = id
        self.from_id = from_id
        self.to_id = to_id

    @staticmethod
    def from_shape(shape: Shape):
        connected_shapes = shape.connects
        if connected_shapes[0].from_rel == 'BeginX':
            return VisioConnector(shape.ID, connected_shapes[0].shape_id, connected_shapes[1].shape_id)
        else:
            return VisioConnector(shape.ID, connected_shapes[1].shape_id, connected_shapes[0].shape_id)

    def __str__(self) -> str:
        return super().__str__()


class VisioDiagram:
    components: [VisioComponent]
    connectors: [VisioConnector]

    def __init__(self, components: [VisioComponent], connectors: [VisioConnector]):
        self.components = components
        self.connectors = connectors
