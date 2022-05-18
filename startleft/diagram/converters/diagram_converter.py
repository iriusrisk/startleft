from abc import abstractmethod

from startleft.diagram.objects.diagram_objects import Diagram


class DiagramConverter:

    @abstractmethod
    def convert_to_diagram(self, diagram_source) -> Diagram:
        pass
