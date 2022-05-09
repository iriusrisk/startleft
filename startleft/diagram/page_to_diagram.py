from vsdx import Page, Shape

from startleft.diagram.parent_calculator import ParentCalculator
from startleft.diagram.visio_objects import VisioComponent, VisioConnector, VisioDiagram


def is_connector(shape) -> bool:
    for connect in shape.connects:
        if shape.ID == connect.connector_shape_id:
            return True

    return False


def is_component(shape) -> bool:
    return shape.text and not is_connector(shape)


class PageToDiagram:
    def __init__(self, page: Page):
        self.page = page
        self.__visio_components = []
        self.__visio_connectors = []

    def run(self):
        self.__load_page_elements()
        self.__calculate_parents()
        return VisioDiagram(self.__visio_components, self.__visio_connectors)

    def __load_page_elements(self):
        page_shapes = []

        for shape in self.page.sub_shapes():
            if is_connector(shape):
                self.__add_visio_connector(shape)
            elif is_component(shape):
                self.__add_visio_component(shape)

        return page_shapes

    def __add_visio_component(self, component_shape: Shape):
        self.__visio_components.append(VisioComponent.from_shape(component_shape))

    def __add_visio_connector(self, connector_shape: Shape):
        self.__visio_connectors.append(VisioConnector.from_shape(connector_shape))

    def __calculate_parents(self):
        for component in self.__visio_components:
            component.parent = ParentCalculator(component).calculate_parent(self.__visio_components)

