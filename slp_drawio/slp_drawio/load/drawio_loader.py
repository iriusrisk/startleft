import logging

from slp_base import LoadingSourceFileError, CommonError
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

    def __init__(self, project_id: str, source):
        self.project_id = project_id
        self.source = source
        self.diagram = None

    def load(self):
        try:
            source_dict = DrawIOToDict(self.source).to_dict()

            representation: DiagramRepresentation = DiagramRepresentationLoader(self.project_id, source_dict).load()
            components: [DiagramComponent] = DiagramComponentLoader(self.project_id, source_dict).load()
            dataflows: [DiagramDataflow] = DiagramDataflowLoader(source_dict).load()

            self.diagram: Diagram = Diagram(representation, components, dataflows)
        except CommonError as e:
            raise e
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingSourceFileError('Source file cannot be loaded', detail, message)

    def get_diagram(self) -> Diagram:
        return self.diagram
