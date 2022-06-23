import logging

import yaml
from deepmerge import always_merger

from startleft.api.errors import LoadingMappingFileError
from startleft.validators.mapping_validator import MappingValidator

logger = logging.getLogger(__name__)


class MappingFileLoader:

    def __init__(self):
        self.map = {}

    def load(self, mapping_data_list: [bytes]) -> {}:

        MappingValidator.check_data_size(mapping_data_list[0])

        try:
            for mapping_data in mapping_data_list:
                logger.info('Loading mapping data')
                data = mapping_data if isinstance(mapping_data, str) else mapping_data.decode()
                self.__load(yaml.load(data, Loader=yaml.BaseLoader))
                logger.debug('Mapping files loaded successfully')
        except Exception as e:
            raise LoadingMappingFileError('Error loading the mapping file. The mapping file is not valid.',
                                          e.__class__.__name__, str(e))
        return self.map

    def __load(self, mapping):
        always_merger.merge(self.map, mapping)
