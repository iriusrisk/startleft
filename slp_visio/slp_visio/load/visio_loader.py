import logging

from slp_base import DiagramType, DiagramFileNotValidError, ProviderLoader, LoadingDiagramFileError
from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from slp_visio.slp_visio.load.vsdx_parser import VsdxParser

logger = logging.getLogger(__name__)


def get_parser_for_diagram_type(provider):
    if provider == DiagramType.VISIO:
        return VsdxParser(VisioComponentFactory(), VisioConnectorFactory())
    msg = 'Cannot recognize given diagram type'
    raise DiagramFileNotValidError('UnknownDiagramType', msg, f'{msg} {provider}')


def get_diagram_ext(diag_type):
    if diag_type == DiagramType.VISIO:
        return '.vsdx'
    logger.warning(f'Unknown file extension for diagrams {diag_type}')
    return ''


class VisioLoader(ProviderLoader):

    def load(self):
        try:
            self.visio = VsdxParser(VisioComponentFactory(), VisioConnectorFactory()).parse(self.source.name)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingDiagramFileError('Diagram file is not valid', detail, message)

    def __init__(self, source):
        self.visio = None
        self.source = source

    def get_visio(self):
        return self.visio
