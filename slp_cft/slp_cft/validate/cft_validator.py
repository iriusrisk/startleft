import logging

from sl_util.sl_util.file_utils import get_file_type_by_content
from slp_base import IacType
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.errors import IacFileNotValidError
from slp_base.slp_base.provider_validator import generate_content_type_error, generate_size_error

logger = logging.getLogger(__name__)

MAX_SIZE = 1 * 1024 * 1024
MIN_SIZE = 13


class CloudformationValidator(ProviderValidator):

    def __init__(self, cloudformation_data_list: [bytes]):
        super(CloudformationValidator, self).__init__()
        self.cloudformation_data_list = cloudformation_data_list

    def validate(self):
        logger.info('Validating CloudFormation file')
        self.__validate_size()
        self.validate_content_type()

    def __validate_size(self):
        for cft_data in self.cloudformation_data_list:
            size = len(cft_data)
            if size > MAX_SIZE or size < MIN_SIZE:
                raise generate_size_error(IacType.CLOUDFORMATION, 'iac_file', IacFileNotValidError)

    def validate_content_type(self):
        for cft_data in self.cloudformation_data_list:
            if get_file_type_by_content(cft_data) not in IacType.CLOUDFORMATION.valid_mime:
                raise generate_content_type_error(IacType.CLOUDFORMATION, 'iac_file', IacFileNotValidError)
