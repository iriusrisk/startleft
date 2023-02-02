import logging

from slp_visio.slp_visio.load.visio_loader import VisioLoader
from slp_visio.slp_visio.lucid.load.objects.lucid_diagram_factories import LucidComponentFactory, LucidConnectorFactory
from slp_visio.slp_visio.lucid.load.lucid_vsdx_parser import LucidVsdxParser

logger = logging.getLogger(__name__)


class LucidLoader(VisioLoader):

    def __init__(self, source):
        super().__init__(source)
        self.parser = LucidVsdxParser(LucidComponentFactory(), LucidConnectorFactory())
