from abc import abstractmethod

from startleft.diagram.objects.diagram_objects import Diagram


class DiagramParser:

    @abstractmethod
    def parse(self, diagram_source) -> Diagram:
        pass
