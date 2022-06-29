import logging

import magic as magik

from startleft.api.errors import IacFileNotValidError
from startleft.iac.iac_type import IacType

logger = logging.getLogger(__name__)

cft_valid_mime = ('application/json', 'text/yaml', 'text/plain')
tf_valid_mime = ('text/plain')

MAX_SIZE = 5 * 1024 * 1024
MIN_SIZE = 5


class IacValidator:

    def __init__(self, iac_data_list: [bytes], iac_type: IacType):
        if iac_type is None:
            raise ValueError("Validation error iac type is void")
        if iac_data_list is None or iac_data_list == []:
            raise ValueError("Validation error iac file is void")
        self.iac_type = iac_type
        self.iac_data_list = iac_data_list

    def __validate_content_type(self, valid):
        for iac_data in self.iac_data_list:
            magic = magik.Magic(mime=True)
            mime = magic.from_buffer(iac_data)
            if mime not in valid:
                msg = 'IaC file is not valid. Invalid content type for iac_file'
                raise IacFileNotValidError("IaC file is not valid", msg, msg)

    def __validate_cloudformation(self):
        self.__validate_content_type(cft_valid_mime)

    def __validate_terraform(self):
        self.__validate_content_type(tf_valid_mime)

    def __validate_size(self):
        for iac_data in self.iac_data_list:
            size = len(iac_data)
            if size is None or size > MAX_SIZE or size < MIN_SIZE:
                msg = 'IaC file is not valid. Invalid size'
                raise IacFileNotValidError('IaC file is not valid', msg, msg)

    def validate(self):
        logger.debug("Validating iac files")
        self.__validate_size()
        if self.iac_type is IacType.CLOUDFORMATION:
            self.__validate_cloudformation()
        elif self.iac_type is IacType.TERRAFORM:
            self.__validate_terraform()
