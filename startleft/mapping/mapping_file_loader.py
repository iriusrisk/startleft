import logging

import yaml
from deepmerge import always_merger

from startleft.api.errors import MappingFileNotFoundError

logger = logging.getLogger(__name__)


class MappingFileLoader:

    def __init__(self):
        self.map = {}

    def load(self, filenames) -> {}:
        if isinstance(filenames, str):
            filenames = [filenames]
        for filename in filenames:
            logger.debug(f"Loading mapping file {filename}")
            try:
                if isinstance(filename, str):
                    with open(filename, 'r') as f:
                        self.__load(yaml.load(f, Loader=yaml.BaseLoader))
                else:
                    self.__load(yaml.load(filename, Loader=yaml.BaseLoader))
            except FileNotFoundError:
                logger.warning(f"Cannot find mapping file '{filename}'")
                raise MappingFileNotFoundError()

        return self.map

    def __load(self, mapping):
        logger.debug('Loading mapping file')
        always_merger.merge(self.map, mapping)
