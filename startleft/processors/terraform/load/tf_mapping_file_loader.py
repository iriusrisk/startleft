import logging

import yaml
from deepmerge import always_merger

from startleft.api.errors import LoadingMappingFileError
from startleft.processors.base.mapping import MappingLoader

logger = logging.getLogger(__name__)


class TerraformMappingFileLoader(MappingLoader):

    def __init__(self, mapping_files_data: [bytes]):
        self.mapping_files = mapping_files_data
        self.map = {}

    def load(self) -> {}:
        try:
            for mapping_file_data in self.mapping_files:
                logger.info('Loading mapping data')
                data = mapping_file_data if isinstance(mapping_file_data, str) else mapping_file_data.decode()
                self.__load(yaml.load(data, Loader=yaml.BaseLoader))
                logger.debug('Mapping files loaded successfully')
        except Exception as e:
            raise LoadingMappingFileError('Error loading the TF mapping file. The mapping files are not valid.',
                                          e.__class__.__name__, str(e))
        return self.map

    def get_mappings(self):
        return self.map

    def __load(self, mapping):
        always_merger.merge(self.map, mapping)
