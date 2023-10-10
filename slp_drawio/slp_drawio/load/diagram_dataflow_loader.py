from slp_drawio.slp_drawio.objects.diagram_objects import DiagramDataflow


class DiagramDataflowLoader:

    def __init__(self, source: dict):
        self.source: dict = source

    def load_dataflows(self) -> [DiagramDataflow]:
        return []
