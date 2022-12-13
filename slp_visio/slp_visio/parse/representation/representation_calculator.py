from otm.otm.otm import RepresentationElement
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits, DiagramComponent


class RepresentationCalculator:

    def __init__(self, diagram_representation_id: str, limits: DiagramLimits):
        self.diagram_representation_id = diagram_representation_id
        self.limits = limits

    def calculate_representation(self, component: DiagramComponent) -> RepresentationElement:
        pass
