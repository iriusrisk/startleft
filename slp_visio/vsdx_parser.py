from vsdx import Shape, VisioFile

from slp_visio.diagram_parser import DiagramParser
from slp_visio.diagram_type import DiagramType
from slp_visio.objects.diagram_objects import Diagram, DiagramComponentOrigin, DiagramLimits
from slp_visio.parsing.parent_calculator import ParentCalculator
from slp_visio.representation.visio.simple_component_representer import SimpleComponentRepresenter
from slp_visio.representation.visio.zone_component_representer import ZoneComponentRepresenter
from slp_visio.util.visio import get_limits
from slp_visio.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory

DIAGRAM_LIMITS_PADDING = 2


def load_visio_page_from_file(visio_filename: str):
    with VisioFile(visio_filename) as vis:
        return vis.pages[0].shapes[0]


def is_connector(shape: Shape) -> bool:
    for connect in shape.connects:
        if shape.ID == connect.connector_shape_id:
            return True

    return False


def is_component(shape: Shape) -> bool:
    return shape.text and not is_connector(shape)


def is_boundary(shape: Shape) -> bool:
    return shape.shape_name is not None and 'Curved panel' in shape.shape_name


class VsdxParser(DiagramParser):

    def __init__(self, component_factory: VisioComponentFactory, connector_factory: VisioConnectorFactory):
        self.component_factory = component_factory
        self.connector_factory = connector_factory

        self.__zone_representer = None
        self.__component_representer = None

        self.page = None
        self.__visio_components = []
        self.__visio_connectors = []

    def parse(self, visio_diagram_filename) -> Diagram:
        self.page = load_visio_page_from_file(visio_diagram_filename)

        diagram_limits = self.__calculate_diagram_limits()
        self.__component_representer = SimpleComponentRepresenter()
        self.__zone_representer = ZoneComponentRepresenter(diagram_limits)

        self.__load_page_elements()
        self.__calculate_parents()

        return Diagram(DiagramType.VISIO, self.__visio_components, self.__visio_connectors, diagram_limits)

    def __calculate_diagram_limits(self) -> DiagramLimits:
        floor_coordinates = [None, None]
        top_coordinates = [0, 0]

        for shape_limits in map(get_limits, self.page.sub_shapes()):
            if not floor_coordinates[0] or shape_limits[0][0] < floor_coordinates[0]:
                floor_coordinates[0] = shape_limits[0][0] - DIAGRAM_LIMITS_PADDING

            if not floor_coordinates[1] or shape_limits[0][1] < floor_coordinates[1]:
                floor_coordinates[1] = shape_limits[0][1] - DIAGRAM_LIMITS_PADDING

            if shape_limits[1][0] > top_coordinates[0]:
                top_coordinates[0] = shape_limits[1][0] + DIAGRAM_LIMITS_PADDING

            if shape_limits[1][1] > top_coordinates[1]:
                top_coordinates[1] = shape_limits[1][1] + DIAGRAM_LIMITS_PADDING

        return DiagramLimits([floor_coordinates, top_coordinates])

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
            self.component_factory.create_component(
                component_shape, DiagramComponentOrigin.SIMPLE_COMPONENT, self.__component_representer))

    def __add_boundary_component(self, component_shape: Shape):
        self.__visio_components.append(
            self.component_factory.create_component(
                component_shape, DiagramComponentOrigin.BOUNDARY, self.__zone_representer))

    def __add_connector(self, connector_shape: Shape):
        visio_connector = self.connector_factory.create_connector(connector_shape)
        if visio_connector:
            self.__visio_connectors.append(visio_connector)

    def __calculate_parents(self):
        for component in self.__visio_components:
            component.parent = ParentCalculator(component).calculate_parent(self.__visio_components)
