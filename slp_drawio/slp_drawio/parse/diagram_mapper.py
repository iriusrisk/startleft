from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramRepresentation


class DiagramMapper:
    def __init__(self, project_id: str, diagram: Diagram, mapping: DrawioMapping):
        self.project_id = project_id
        self.diagram = diagram
        self.mapping = mapping
        self.size = {'x': 1000, 'y': 1000}

    def map(self):
        self.diagram.representation = DiagramRepresentation(self.project_id, self.size)
