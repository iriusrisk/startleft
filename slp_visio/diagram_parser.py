from abc import abstractmethod

from slp_visio.objects.diagram_objects import Diagram


class DiagramParser:

    @abstractmethod
    def parse(self, diagram_source) -> Diagram:
        pass
