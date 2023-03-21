import logging
import os
from zipfile import ZipFile

import magic as magik

from slp_base import ProviderValidator, DiagramFileNotValidError, DiagramType
from slp_base.slp_base.provider_validator import generate_content_type_error, generate_size_error

logger = logging.getLogger(__name__)

MAX_SIZE = 10 * 1024 * 1024
MIN_SIZE = 10


class VisioValidator(ProviderValidator):

    def __init__(self, file, provider=DiagramType.VISIO):
        self.file = file
        self.provider = provider

    def validate(self):
        logger.info('Validating visio file')
        self.__validate_size()
        self.__validate_content_type()
        self.__validate_zip_content()

    def __validate_size(self):
        size = os.path.getsize(self.file.name)
        if size > MAX_SIZE or size < MIN_SIZE:
            raise generate_size_error(self.provider, 'diag_file', DiagramFileNotValidError)

    def __get_mime_type(self):
        magic = magik.Magic(mime=True)
        return magic.from_file(self.file.name)

    def __validate_content_type(self):
        mime = self.__get_mime_type()
        if mime not in self.provider.valid_mime:
            raise generate_content_type_error(self.provider, 'diag_file', DiagramFileNotValidError)

    def __validate_zip_content(self):
        mime = self.__get_mime_type()
        if 'application/zip' == mime:
            with ZipFile(self.file.name) as myzip:
                if not any("[Content_Types].xml" == file.filename for file in myzip.filelist):
                    raise generate_content_type_error(self.provider, 'diag_file', DiagramFileNotValidError)
