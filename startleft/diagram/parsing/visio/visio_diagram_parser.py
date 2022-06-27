from vsdx import Shape, VisioFile

from startleft.diagram.diagram_type import DiagramType
from startleft.diagram.objects.diagram_objects import Diagram, DiagramComponentOrigin
from startleft.diagram.objects.visio.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from startleft.diagram.parsing.diagram_parser import DiagramParser
from startleft.diagram.parsing.parent_calculator import ParentCalculator


def load_visio_page_from_file(visio_filename: str):
    with VisioFile(visio_filename) as vis:
        return vis.pages[0].shapes[0]


def get_shape_coordinates(shape: Shape) -> tuple:
    return float(shape.cells['PinX'].value), float(shape.cells['PinY'].value)


def is_connector(shape: Shape) -> bool:
    for connect in shape.connects:
        if shape.ID == connect.connector_shape_id:
            return True

    return False


def is_component(shape: Shape) -> bool:
    return shape.text and not is_connector(shape)


def is_boundary(shape: Shape) -> bool:
    return shape.shape_name is not None and 'Curved panel' in shape.shape_name


class VisioDiagramParser(DiagramParser):

    def __init__(self, component_factory: VisioComponentFactory, connector_factory: VisioConnectorFactory):
        self.component_factory = component_factory
        self.connector_factory = connector_factory

        self.page = None
        self.__visio_components = []
        self.__visio_connectors = []

    def parse(self, visio_diagram_filename) -> Diagram:
        self.page = load_visio_page_from_file(visio_diagram_filename)

        self.component_factory.set_diagram_limits(self.__calculate_diagram_limits())

        self.__load_page_elements()
        self.__calculate_parents()

        return Diagram(DiagramType.VISIO, self.__visio_components, self.__visio_connectors)

    def __calculate_diagram_limits(self) -> tuple:
        limit_coordinates = [0, 0]

        for shape_coordinates in map(get_shape_coordinates, self.page.sub_shapes()):
            if shape_coordinates[0] > limit_coordinates[0]:
                limit_coordinates[0] = shape_coordinates[0]

            if shape_coordinates[1] > limit_coordinates[1]:
                limit_coordinates[1] = shape_coordinates[1]

        return tuple(limit_coordinates)

    def __load_page_elements(self):
        for shape in self.page.sub_shapes():
            if is_connector(shape):
                self.__add_connector(shape)
            elif is_boundary(shape):
                self.__add_boundary_component(shape)
            elif is_component(shape):
                self.__add_simple_component(shape)

    def __add_simple_component(self, component_shape: Shape):
        self.__visio_components.append(
            self.component_factory.create_component(component_shape, DiagramComponentOrigin.SIMPLE_COMPONENT))

    def __add_boundary_component(self, component_shape: Shape):
        self.__visio_components.append(
            self.component_factory.create_component(component_shape, DiagramComponentOrigin.BOUNDARY))

    def __add_connector(self, connector_shape: Shape):
        self.__visio_connectors.append(self.connector_factory.create_connector(connector_shape))

    def __calculate_parents(self):
        for component in self.__visio_components:
            component.parent = ParentCalculator(component).calculate_parent(self.__visio_components)

