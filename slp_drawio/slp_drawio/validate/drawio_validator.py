import copy
import logging
import os
import string
import uuid

import xmlschema

from slp_base import ProviderValidator, DiagramFileNotValidError, DiagramType
from slp_base.slp_base.provider_validator import generate_size_error, generate_content_type_error, generate_schema_error

logger = logging.getLogger(__name__)

MAX_SIZE = 10 * 1024 * 1024
MIN_SIZE = 10

path = os.path.dirname(__file__)


class DrawioValidator(ProviderValidator):

    def __init__(self, data):
        super(DrawioValidator, self).__init__()
        self.data = data
        self.provider = DiagramType.DRAWIO
        self.xsd_schema = f'{path}/../../resources/schemas/drawio_schema.xsd'

    def validate(self):
        logger.info('Validating Drawio file')
        self.__validate_size()
        self.__validate_content_type()
        self.__sanitize_name()
        self.__validate_schema()

    def __validate_size(self):
        size = self.data.size
        if size > MAX_SIZE or size < MIN_SIZE:
            raise generate_size_error(self.provider, 'diag_file', DiagramFileNotValidError)

    def __validate_content_type(self):
        mime = self.data.content_type
        if mime not in self.provider.valid_mime:
            raise generate_content_type_error(self.provider, 'diag_file', DiagramFileNotValidError)

    def __sanitize_name(self):
        ext = self.data.filename.split('.')[-1]
        ext = "".join([c for c in ext if c in string.ascii_letters])
        name = str(uuid.uuid4())
        self.data.filename = f'{name}.{ext}'

    def __validate_schema(self):
        schema = xmlschema.XMLSchema(self.xsd_schema)
        try:
            file_copy = copy.deepcopy(self.data.file)
            schema.validate(file_copy)
        except Exception:
            raise generate_schema_error(self.provider, 'diag_file', DiagramFileNotValidError)
