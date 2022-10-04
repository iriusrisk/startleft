import logging

import magic as magik

from slp_base import ProviderValidator
from slp_base.slp_base.errors import SourceFileNotValidError

logger = logging.getLogger(__name__)

VALID_MIME = ['application/xml', 'text/plain']

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
            msg = 'Provided MTMT file is not valid. Invalid size'
            raise SourceFileNotValidError('TM file is not valid', msg, msg)

    def __validate_content_type(self):
        magic = magik.Magic(mime=True)
        mime = magic.from_buffer(self.mt_data)
        if mime not in VALID_MIME:
            msg = 'Invalid content type for diag_file'
            raise SourceFileNotValidError('TM file is not valid', msg, msg)
