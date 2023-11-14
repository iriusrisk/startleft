from slp_drawio.slp_drawio.load.drawio_dict_utils import get_diagram_size
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramRepresentation

DEFAULT_SIZE = {'width': 1000, 'height': 1000}


class DiagramRepresentationLoader:

    def __init__(self, project_id: str, source: dict):
        self._project_id = project_id
        self._source = source

    def load(self) -> DiagramRepresentation:
        return DiagramRepresentation(
            project_id=self._project_id,
            size=get_diagram_size(self._source) or DEFAULT_SIZE)
