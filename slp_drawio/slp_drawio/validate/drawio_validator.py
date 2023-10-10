import logging

from slp_base import ProviderValidator

logger = logging.getLogger(__name__)


class DrawioValidator(ProviderValidator):

    def __init__(self, data):
        super(DrawioValidator, self).__init__()
        self.data = data

    def validate(self):
        logger.info('Validating Drawio file')
        self.__validate_size()
        self.__validate_content_type()

    def __validate_size(self):
        pass

    def __validate_content_type(self):
        pass
