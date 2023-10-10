import logging

from slp_base import LoadingSourceFileError
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_drawio.slp_drawio.load.diagram_component_loader import DiagramComponentLoader
from slp_drawio.slp_drawio.load.diagram_dataflow_loader import DiagramDataflowLoader
from slp_drawio.slp_drawio.load.diagram_representation_loader import DiagramRepresentationLoader
from slp_drawio.slp_drawio.load.drawio_to_dict import DrawIOToDict
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramDataflow, DiagramComponent, \
    DiagramRepresentation

logger = logging.getLogger(__name__)


class DrawioLoader(ProviderLoader):
    """
    Builder for a drawio class from the xml data
    """

    def load(self):
        try:
            source = DrawIOToDict(self.source).to_dict()

            representation: DiagramRepresentation = DiagramRepresentationLoader(self.project_id, source).load()
            components: [DiagramComponent] = DiagramComponentLoader(source).load()
            dataflows: [DiagramDataflow] = DiagramDataflowLoader(source).load()

            self.diagram: Diagram = Diagram(representation, components, dataflows)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingSourceFileError('Source file cannot be loaded', detail, message)

    def __init__(self, project_id: str, source):
        self.project_id = project_id
        self.source = source
        self.diagram = None

    def get_diagram(self) -> Diagram:
        return self.diagram
