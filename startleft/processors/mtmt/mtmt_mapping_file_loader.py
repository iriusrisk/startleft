from startleft.processors.base.mapping import MappingLoader
from deepmerge import always_merger
from startleft.api.errors import LoadingMappingFileError
import yaml
import logging
import jmespath
from startleft import messages

logger = logging.getLogger(__name__)


class MTMTMapping:

    def __init__(self, trustzones, components, dataflows):
        self.mapping_trustzones = trustzones
        self.mapping_components = components
        self.mapping_dataflows = dataflows


class MTMTMappingFileLoader(MappingLoader):

    def __init__(self, mapping_data_list: [bytes]):
        self.mappings = mapping_data_list
        self.map = {}
        self.mtmt_mapping = None

    def load(self):
        try:
            self.__merge_mapping(self.mappings)
            self.mtmt_mapping = MTMTMapping(
                self.__get_trustzones(),
                self.__get_components(),
                []
            )
        except Exception as e:
            raise LoadingMappingFileError('Error loading the mapping file. The mapping files are not valid.',
                                          e.__class__.__name__, str(e))

    def __get_trustzones(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.map)
        return dict(zip([tz['label'] for tz in trustzone_mappings_list], trustzone_mappings_list))

    def __get_components(self):
        component_mappings_list = jmespath.search("components", self.map)
        return dict(zip([tz['label'] for tz in component_mappings_list], component_mappings_list))

    def __merge_mapping(self, mapping):
        for mapping_data in self.mappings:
            logger.info('Loading mapping data')
            data = mapping_data if isinstance(mapping_data, str) else mapping_data.decode()
            always_merger.merge(self.map, yaml.load(data, Loader=yaml.BaseLoader))
            logger.debug('Mapping files loaded successfully')

    def get_mtmt_mapping(self):
        return self.mtmt_mapping
