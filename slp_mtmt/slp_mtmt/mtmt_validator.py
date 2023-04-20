import logging

import magic as magik

from slp_base import ProviderValidator, EtmType
from slp_base.slp_base.provider_validator import generate_content_type_error, generate_size_error

logger = logging.getLogger(__name__)

MAX_SIZE = 20 * 1024 * 1024
MIN_SIZE = 20


class MTMTValidator(ProviderValidator):

    def __init__(self, mt_data):
        super(MTMTValidator, self).__init__()
        self.mt_data = mt_data

    def validate(self):
        logger.info('Validating MTMT file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        size = len(self.mt_data)
        if size > MAX_SIZE or size < MIN_SIZE:
            raise generate_size_error(EtmType.MTMT, 'source_file')

    def __validate_content_type(self):
        magic = magik.Magic(mime=True)
        mime = magic.from_buffer(self.mt_data)
        if mime not in EtmType.MTMT.valid_mime:
            raise generate_content_type_error(EtmType.MTMT, 'source_file')
