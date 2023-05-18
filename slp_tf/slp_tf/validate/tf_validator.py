import logging

from sl_util.sl_util.file_utils import get_file_type_by_content

from slp_base import IacFileNotValidError, IacType
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.provider_validator import generate_size_error, generate_content_type_error

logger = logging.getLogger(__name__)

VALID_MIME = ['text/plain', 'application/octet-stream', 'application/json']

MAX_SIZE = 1024 * 1024  # 1MB
MIN_SIZE = 20


class TerraformValidator(ProviderValidator):

    def __init__(self, terraform_data_list: [bytes]):
        super(TerraformValidator, self).__init__()
        self.terraform_data_list = terraform_data_list

    def validate(self):
        logger.info('Validating Terraform file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        for tf_data in self.terraform_data_list:
            size = len(tf_data)
            if size > MAX_SIZE or size < MIN_SIZE:
                raise generate_size_error(IacType.TERRAFORM, 'iac_file', IacFileNotValidError)

    def __validate_content_type(self):
        for tf_data in self.terraform_data_list:
            if get_file_type_by_content(tf_data) not in IacType.TERRAFORM.valid_mime:
                raise generate_content_type_error(IacType.TERRAFORM, 'iac_file', IacFileNotValidError)
