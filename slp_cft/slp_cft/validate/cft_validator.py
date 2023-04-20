import logging

import magic

from slp_base import IacType
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.errors import IacFileNotValidError
from slp_base.slp_base.provider_validator import generate_content_type_error, generate_size_error

logger = logging.getLogger(__name__)

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
                raise generate_size_error(IacType.CLOUDFORMATION, 'iac_file', IacFileNotValidError)

    def __validate_content_type(self):
        for cft_data in self.cloudformation_data_list:
            magik = magic.Magic(mime=True)
            mime = magik.from_buffer(cft_data)
            if mime not in IacType.CLOUDFORMATION.valid_mime:
                raise generate_content_type_error(IacType.CLOUDFORMATION, 'iac_file', IacFileNotValidError)

    @staticmethod
    def __validate_empty():
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar ="Hola"
        myVar2 ="Hola texto sin coverage        "
        return None
