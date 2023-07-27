from vsdx import Shape, VisioFile

from slp_base import DiagramType
from slp_visio.slp_visio.load.boundary_identifier import BoundaryIdentifier
from slp_visio.slp_visio.load.component_identifier import ComponentIdentifier
from slp_visio.slp_visio.load.connector_identifier import ConnectorIdentifier
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponentOrigin, DiagramLimits
from slp_visio.slp_visio.load.parent_calculator import ParentCalculator
from slp_visio.slp_visio.load.representation.simple_component_representer import SimpleComponentRepresenter
from slp_visio.slp_visio.load.representation.zone_component_representer import ZoneComponentRepresenter
from slp_visio.slp_visio.util.visio import get_limits

DIAGRAM_LIMITS_PADDING = 2
DEFAULT_DIAGRAM_LIMITS = DiagramLimits(((1000, 1000), (1000, 1000)))


def load_visio_page_from_file(visio_filename: str):
    with VisioFile(visio_filename) as vis:
        return vis.pages[0]


class VsdxParser:

    def __init__(self, component_factory, connector_factory):
        self.component_factory = component_factory
        self.connector_factory = connector_factory

        self.__zone_representer = None
        self._component_representer = None

        self.page = None
        self._visio_components = []
        self._visio_connectors = []
        self.component_identifier = ComponentIdentifier()
        self.connector_identifier = ConnectorIdentifier()
        self.boundary_identifier = BoundaryIdentifier()

    def parse(self, visio_diagram_filename) -> Diagram:
        self.page = load_visio_page_from_file(visio_diagram_filename)

        diagram_limits = self.__calculate_diagram_limits()
        self._component_representer = SimpleComponentRepresenter()
        self.__zone_representer = ZoneComponentRepresenter(diagram_limits)

        self._load_page_elements()
        self._calculate_parents()

        return Diagram(DiagramType.VISIO, self._visio_components, self._visio_connectors, diagram_limits)

    def __calculate_diagram_limits(self) -> DiagramLimits:
        floor_coordinates = [None, None]
        top_coordinates = [0, 0]

        for shape_limits in map(get_limits, self.page.child_shapes):
            if not floor_coordinates[0] or shape_limits[0][0] < floor_coordinates[0]:
                floor_coordinates[0] = shape_limits[0][0] - DIAGRAM_LIMITS_PADDING

            if not floor_coordinates[1] or shape_limits[0][1] < floor_coordinates[1]:
                floor_coordinates[1] = shape_limits[0][1] - DIAGRAM_LIMITS_PADDING

            if shape_limits[1][0] > top_coordinates[0]:
                top_coordinates[0] = shape_limits[1][0] + DIAGRAM_LIMITS_PADDING

            if shape_limits[1][1] > top_coordinates[1]:
                top_coordinates[1] = shape_limits[1][1] + DIAGRAM_LIMITS_PADDING

        return DiagramLimits([floor_coordinates, top_coordinates]) \
            if floor_coordinates[0] and floor_coordinates[1] \
            else DEFAULT_DIAGRAM_LIMITS

    def _load_page_elements(self):
            self._load_shapes(self.page.child_shapes)

    def _load_shapes(self, shapes: [Shape]):
        for shape in shapes:
            self._load_shape(shape)

    def _load_shape(self, shape: Shape):
        if self.connector_identifier.is_connector(shape):
            self._add_connector(shape)
        elif self.boundary_identifier.is_boundary(shape):
            self._add_boundary_component(shape)
        elif self.component_identifier.is_component(shape):
            self._add_simple_component(shape)
        elif self._is_group(shape):
            self._load_shapes(shape.child_shapes)

    def _add_simple_component(self, component_shape: Shape):
        self._visio_components.append(
            self.component_factory.create_component(
                component_shape, DiagramComponentOrigin.SIMPLE_COMPONENT, self._component_representer))

    def _add_boundary_component(self, component_shape: Shape):
        self._visio_components.append(
            self.component_factory.create_component(
                component_shape, DiagramComponentOrigin.BOUNDARY, self.__zone_representer))

    def _add_connector(self, connector_shape: Shape):
        visio_connector = self.connector_factory.create_connector(connector_shape)
        if visio_connector:
            self._visio_connectors.append(visio_connector)

    def _calculate_parents(self):
        for component in self._visio_components:
            component.parent = ParentCalculator(component).calculate_parent(self._visio_components)

    @staticmethod
    def _is_group(shape : Shape):
        return shape.shape_type == 'Group'
