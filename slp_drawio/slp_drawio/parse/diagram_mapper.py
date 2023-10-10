from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram


class DiagramMapper:
    def __init__(self, diagram: Diagram, mapping: DrawioMapping):
        self.diagram = diagram
        self.mapping = mapping

    def map(self):
        pass
