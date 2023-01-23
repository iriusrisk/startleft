import logging

import magic

from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.errors import IacFileNotValidError

logger = logging.getLogger(__name__)

VALID_MIME = ('application/json', 'text/yaml', 'text/plain', 'application/octet-stream')

MAX_SIZE = 20 * 1024 * 1024
MIN_SIZE = 13


class CloudformationValidator(ProviderValidator):

    def __init__(self, cloudformation_data_list: [bytes]):
        super(CloudformationValidator, self).__init__()
        self.cloudformation_data_list = cloudformation_data_list

    def validate(self):
        logger.info('Validating CloudFormation file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        for cft_data in self.cloudformation_data_list:
            size = len(cft_data)
            if size > MAX_SIZE or size < MIN_SIZE:
                msg = 'CloudFormation file is not valid. Invalid size'
                raise IacFileNotValidError('CloudFormation file is not valid', msg, msg)

    def __validate_content_type(self):
        for cft_data in self.cloudformation_data_list:
            magik = magic.Magic(mime=True)
            mime = magik.from_buffer(cft_data)
            if mime not in VALID_MIME:
                msg = 'CloudFormation file is not valid. Invalid content type for iac_file'
                raise IacFileNotValidError('CloudFormation file is not valid', msg, msg)
