import logging
import os

logger = logging.getLogger(__name__)


class LogSecurityFilter(logging.Filter):

    def __init__(self, max_msg_size):
        super().__init__()
        self.my_name = os.path.basename(__file__)
        self.max_msg_size = max_msg_size

    def filter(self, record):
        return self.__filter_size(record)

    def __filter_size(self, record):
        if record.filename == self.my_name:
            return True

        message = record.getMessage()
        size = len(message)

        if size > self.max_msg_size:
            cut_msg = message[0:self.max_msg_size]
            logger.warning(f'The log msg size {size} is greater than the limit {self.max_msg_size}. '
                           f'The msg was: {cut_msg} ''{...''}')
            return False

        return True
