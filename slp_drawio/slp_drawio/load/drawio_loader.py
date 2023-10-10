import logging

from slp_base import LoadingSourceFileError
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_drawio.slp_drawio.load.diagram_component_loader import DiagramComponentLoader
from slp_drawio.slp_drawio.load.diagram_dataflow_loader import DiagramDataflowLoader
from slp_drawio.slp_drawio.load.drawio_to_dict import DrawIOToDict
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramDataflow, DiagramComponent

logger = logging.getLogger(__name__)


class DrawioLoader(ProviderLoader):
    """
    Builder for a drawio class from the xml data
    """

    def load(self):
        try:
            source = DrawIOToDict(self.source).to_dict()
            components: [DiagramComponent] = DiagramComponentLoader(source)
            dataflows: [DiagramDataflow] = DiagramDataflowLoader(source)
            self.diagram: Diagram = Diagram(components, dataflows)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingSourceFileError('Source file cannot be loaded', detail, message)

    def __init__(self, source):
        self.source = source
        self.diagram = None

    def get_diagram(self) -> Diagram:
        return self.diagram
