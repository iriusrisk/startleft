import logging

import yaml
from deepmerge import always_merger

from startleft.api.errors import OTMFileNotFoundError

logger = logging.getLogger(__name__)


class OtmFileLoader:

    def __init__(self):
        self.map = {}

    def load(self, filenames) -> {}:
        otm = {}

        if isinstance(filenames, str):
            filenames = [filenames]

        for filename in filenames:
            logger.debug(f"Loading OTM file {filename}")
            try:
                with open(filename, 'r') as f:
                    self.__load_otm_file(otm, yaml.load(f, Loader=yaml.BaseLoader))
            except FileNotFoundError:
                logger.error(f"Cannot find OTM file '{filename}'")
                raise OTMFileNotFoundError()
        return otm

    def __load_otm_file(self, otm, data):
        always_merger.merge(otm, data)
