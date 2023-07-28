import logging

import yaml
from deepmerge import always_merger

from slp_base import LoadingMappingFileError
from slp_base.slp_base.mapping import validate_size, MappingLoader

logger = logging.getLogger(__name__)


class MappingFileLoader(MappingLoader):

    def __init__(self, mapping_files_data: [bytes]):
        self.mapping_files = mapping_files_data
        self.map = {}

    def load(self) -> {}:
        if not self.mapping_files:
            msg = "Mapping file is empty"
            raise LoadingMappingFileError("Mapping file is not valid", msg, msg)

        validate_size(self.mapping_files[0])

        try:
            # Here we reverse the list to give higher priority to the custom mapping file
            for mapping_file_data in self.mapping_files[::-1]:
                if not mapping_file_data:
                    continue
                logger.info('Loading mapping data')

                data = mapping_file_data if isinstance(mapping_file_data, str) else mapping_file_data.decode()
                self.__load(yaml.load(data, Loader=yaml.BaseLoader))

                logger.debug('Mapping files loaded successfully')
        except Exception as e:
            raise LoadingMappingFileError('Error loading the mapping file. The mapping files are not valid.',
                                          e.__class__.__name__, str(e))
        return self.map

    def get_mappings(self):
        return self.map

    def __load(self, mapping):
        always_merger.merge(self.map, mapping)
