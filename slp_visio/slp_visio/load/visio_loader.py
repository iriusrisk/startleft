import logging

from slp_base import ProviderLoader, LoadingDiagramFileError
from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from slp_visio.slp_visio.load.vsdx_parser import VsdxParser

logger = logging.getLogger(__name__)


class VisioLoader(ProviderLoader):

    def load(self):
        try:
            self.visio = self.parser.parse(self.source.name)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingDiagramFileError('Diagram file is not valid', detail, message)

    def __init__(self, source):
        self.visio = None
        self.source = source
        self.parser = VsdxParser(VisioComponentFactory(), VisioConnectorFactory())

    def get_visio(self):
        return self.visio
