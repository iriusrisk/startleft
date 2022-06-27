from abc import abstractmethod

from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector


class DiagramComponentFactory:

    @abstractmethod
    def create_component(self, shape, origin) -> DiagramComponent:
        pass

    @abstractmethod
    def set_diagram_limits(self, limit_coordinates: tuple):
        pass


class DiagramConnectorFactory:

    @abstractmethod
    def create_connector(self, shape) -> DiagramConnector:
        pass
