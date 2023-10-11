import logging
from tempfile import SpooledTemporaryFile

from slp_drawio.slp_drawio.load.objects.drawio_wrapper import DrawioWrapper

logger = logging.getLogger(__name__)


class DrawIOToDict:

    def __init__(self, source):
        file: SpooledTemporaryFile = source.file
        self.wrapper = DrawioWrapper(file.read())

    def to_dict(self) -> dict:
        return self.wrapper.json()
