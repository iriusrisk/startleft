import logging
import os

from sl_util.sl_util.file_utils import get_file_type_by_content
from slp_base import ProviderValidator, DiagramFileNotValidError, DiagramType
from slp_base.slp_base.provider_validator import generate_size_error, generate_content_type_error

logger = logging.getLogger(__name__)

MAX_SIZE = 10 * 1024 * 1024
MIN_SIZE = 10

path = os.path.dirname(__file__)


class AbacusValidator(ProviderValidator):

    def __init__(self, data):
        super(AbacusValidator, self).__init__()
        self.data = data
        self.provider = DiagramType.ABACUS

    def validate(self):
        logger.info('Validating Abacus file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        size = len(self.data)
        if size > MAX_SIZE or size < MIN_SIZE:
            raise generate_size_error(self.provider, 'diag_file', DiagramFileNotValidError)

    def __validate_content_type(self):
        mime = get_file_type_by_content(self.data)
        if mime not in self.provider.valid_mime:
            raise generate_content_type_error(self.provider, 'diag_file', DiagramFileNotValidError)
