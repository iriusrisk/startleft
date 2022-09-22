import logging
import os

import magic as magik

from slp_base import ProviderValidator, DiagramFileNotValidError

logger = logging.getLogger(__name__)

VALID_MIME = ['application/vnd.ms-visio.drawing.main+xml', 'application/octet-stream']

MAX_SIZE = 10 * 1024 * 1024
MIN_SIZE = 10


class VisioValidator(ProviderValidator):

    def __init__(self, file):
        self.file = file

    def validate(self):
        logger.info('Validating visio file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        size = os.path.getsize(self.file.name)
        if size > MAX_SIZE or size < MIN_SIZE:
            msg = 'Provided visio file is not valid. Invalid size'
            raise DiagramFileNotValidError('Diagram file is not valid', msg, msg)

    def __validate_content_type(self):
        magic = magik.Magic(mime=True)
        mime = magic.from_file(self.file.name)
        if mime not in VALID_MIME:
            msg = 'Invalid content type for diag_file'
            raise DiagramFileNotValidError('Diagram file is not valid', msg, msg)
