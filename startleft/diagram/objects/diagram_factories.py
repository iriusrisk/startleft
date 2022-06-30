from abc import abstractmethod

from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector


class DiagramComponentFactory:

    @abstractmethod
    def create_component(self, shape, origin, representer) -> DiagramComponent:
        pass


class DiagramConnectorFactory:

    @abstractmethod
    def create_connector(self, shape) -> DiagramConnector:
        pass
