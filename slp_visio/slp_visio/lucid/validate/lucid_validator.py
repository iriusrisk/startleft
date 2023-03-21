from slp_base import DiagramType

from slp_visio.slp_visio.validate.visio_validator import VisioValidator


class LucidValidator(VisioValidator):

    def __init__(self, file):
        super().__init__(file, DiagramType.LUCID)
