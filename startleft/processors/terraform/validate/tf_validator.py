import logging

import magic as magik

from startleft.api.errors import DiagramFileNotValidError, IacFileNotValidError
from startleft.processors.base.provider_validator import ProviderValidator

logger = logging.getLogger(__name__)

VALID_MIME = ['application/xml', 'text/plain']

MAX_SIZE = 20 * 1024 * 1024
MIN_SIZE = 20


class TerraformValidator(ProviderValidator):

    def __init__(self, mt_data):
        super(TerraformValidator, self).__init__()
        self.mt_data = mt_data

    def validate(self):
        logger.info('Validating Terraform file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        size = len(self.mt_data)
        if size > MAX_SIZE or size < MIN_SIZE:
            msg = 'Provided Terraform file is not valid. Invalid size'
            raise IacFileNotValidError('Terraform file is not valid', msg, msg)

    def __validate_content_type(self):
        magic = magik.Magic(mime=True)
        mime = magic.from_buffer(self.mt_data)
        if mime not in VALID_MIME:
            msg = 'Invalid content type for Terraform file'
            raise DiagramFileNotValidError('Terraform file is not valid', msg, msg)
