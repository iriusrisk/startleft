import logging

import magic

from startleft.api.errors import IacFileNotValidError
from startleft.processors.base.provider_validator import ProviderValidator

logger = logging.getLogger(__name__)

VALID_MIME = ('application/json', 'text/yaml', 'text/plain')

MAX_SIZE = 20 * 1024 * 1024
MIN_SIZE = 20


class CloudformationValidator(ProviderValidator):

    def __init__(self, cloudformation_data):
        super(CloudformationValidator, self).__init__()
        self.cloudformation_data = cloudformation_data

    def validate(self):
        logger.info('Validating CloudFormation file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        size = len(self.cloudformation_data)
        if size > MAX_SIZE or size < MIN_SIZE:
            msg = 'CloudFormation file is not valid. Invalid size'
            raise IacFileNotValidError('CloudFormation file is not valid', msg, msg)

    def __validate_content_type(self):
        magik = magic.Magic(mime=True)
        mime = magik.from_buffer(self.cloudformation_data)
        if mime not in VALID_MIME:
            msg = 'CloudFormation file is not valid. Invalid content type for iac_file'
            raise IacFileNotValidError('CloudFormation file is not valid', msg, msg)
