import logging

import magic

from slp_base import IacFileNotValidError
from slp_base.slp_base import ProviderValidator

logger = logging.getLogger(__name__)

VALID_MIME = ('text/plain')

MAX_SIZE = 20 * 1024 * 1024
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
                msg = 'Terraform file is not valid. Invalid size'
                raise IacFileNotValidError('Terraform file is not valid', msg, msg)

    def __validate_content_type(self):
        for tf_data in self.terraform_data_list:
            magik = magic.Magic(mime=True)
            mime = magik.from_buffer(tf_data)
            if mime not in VALID_MIME:
                msg = 'Invalid content type for Terraform file'
                raise IacFileNotValidError('Terraform file is not valid', msg, msg)
