from slp_drawio.slp_drawio.objects.diagram_objects import DiagramRepresentation


class DiagramRepresentationLoader:

    def __init__(self, project_id: str, source: dict):
        self.project_id = project_id
        self.source = source

    def load(self) -> DiagramRepresentation:
        pass
