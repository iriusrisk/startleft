import logging

from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioComponentFactory
from slp_visio.slp_visio.load.visio_loader import VisioLoader
from slp_visio.slp_visio.lucid.load.objects.lucid_diagram_factories import LucidConnectorFactory
from slp_visio.slp_visio.lucid.load.lucid_vsdx_parser import LucidVsdxParser

logger = logging.getLogger(__name__)


class LucidLoader(VisioLoader):

    def __init__(self, source):
        super().__init__(source)
        self.parser = LucidVsdxParser(VisioComponentFactory(), LucidConnectorFactory())
