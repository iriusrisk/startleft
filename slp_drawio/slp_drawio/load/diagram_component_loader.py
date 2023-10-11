from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent


class DiagramComponentLoader:

    def __init__(self, source: dict):
        self.source: dict = source

    def load(self) -> [DiagramComponent]:
        return []
