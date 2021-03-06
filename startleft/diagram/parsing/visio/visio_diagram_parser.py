from vsdx import Shape, VisioFile

from startleft.diagram.diagram_type import DiagramType
from startleft.diagram.objects.diagram_objects import Diagram
from startleft.diagram.objects.visio.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from startleft.diagram.parsing.diagram_parser import DiagramParser
from startleft.diagram.parsing.parent_calculator import ParentCalculator


def load_visio_page_from_file(visio_filename: str):
    with VisioFile(visio_filename) as vis:
        return vis.pages[0].shapes[0]


def is_connector(shape) -> bool:
    for connect in shape.connects:
        if shape.ID == connect.connector_shape_id:
            return True

    return False


def is_component(shape) -> bool:
    return shape.text and not is_connector(shape)


class VisioDiagramParser(DiagramParser):

    def __init__(self, component_factory: VisioComponentFactory, connector_factory: VisioConnectorFactory):
        self.component_factory = component_factory
        self.connector_factory = connector_factory

        self.page = None
        self.__visio_components = []
        self.__visio_connectors = []

    def parse(self, visio_diagram_filename) -> Diagram:
        self.page = load_visio_page_from_file(visio_diagram_filename)

        self.__load_page_elements()
        self.__calculate_parents()

        return Diagram(DiagramType.VISIO, self.__visio_components, self.__visio_connectors)

    def __load_page_elements(self):
        for shape in self.page.sub_shapes():
            if is_connector(shape):
                self.__add_connector(shape)
            elif is_component(shape):
                self.__add_component(shape)

    def __add_component(self, component_shape: Shape):
        self.__visio_components.append(self.component_factory.create_component(component_shape))

    def __add_connector(self, connector_shape: Shape):
        self.__visio_connectors.append(self.connector_factory.create_connector(connector_shape))

    def __calculate_parents(self):
        for component in self.__visio_components:
            component.parent = ParentCalculator(component).calculate_parent(self.__visio_components)

