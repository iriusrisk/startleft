import logging
import os
from zipfile import ZipFile

import magic as magik

from slp_base import ProviderValidator, DiagramFileNotValidError, DiagramType

logger = logging.getLogger(__name__)

MAX_SIZE = 10 * 1024 * 1024
MIN_SIZE = 10


class VisioValidator(ProviderValidator):

    def __init__(self, file, valid_mime=None):
        if valid_mime is None:
            valid_mime = DiagramType.VISIO.valid_mime

        self.file = file
        self.valid_mime = valid_mime

    def validate(self):
        logger.info('Validating visio file')
        self.__validate_size()
        self.__validate_content_type()
        self.__validate_zip_content()

    def __validate_size(self):
        size = os.path.getsize(self.file.name)
        if size > MAX_SIZE or size < MIN_SIZE:
            msg = 'Provided visio file is not valid. Invalid size'
            raise DiagramFileNotValidError('Diagram file is not valid', msg, msg)

    def __get_mime_type(self):
        magic = magik.Magic(mime=True)
        return magic.from_file(self.file.name)

    def __validate_content_type(self):
        mime = self.__get_mime_type()
        if mime not in self.valid_mime:
            msg = 'Invalid content type for diag_file'
            raise DiagramFileNotValidError('Diagram file is not valid', msg, msg)

    def __validate_zip_content(self):
        mime = self.__get_mime_type()
        if 'application/zip' == mime:
            with ZipFile(self.file.name) as myzip:
                if not any("[Content_Types].xml" == file.filename for file in myzip.filelist):
                    msg = 'Invalid content type for diag_file'
                    raise DiagramFileNotValidError('Diagram file is not valid', msg, msg)
