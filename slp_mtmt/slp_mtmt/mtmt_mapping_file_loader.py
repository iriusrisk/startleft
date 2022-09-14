from slp_base import MappingLoader, LoadingMappingFileError
from deepmerge import always_merger
import yaml
import logging
import jmespath

logger = logging.getLogger(__name__)


class MTMTMapping:

    def __init__(self, trustzones, components, dataflows):
        self.mapping_trustzones = trustzones
        self.mapping_components = components
        self.mapping_dataflows = dataflows


class MTMTMappingFileLoader(MappingLoader):

    def __init__(self, mapping_data_list: [bytes]):
        self.provided_mappings = mapping_data_list
        self.merged_mappings = {}
        self.mtmt_mapping = None

    def load(self):
        try:
            self.__merge_mapping()
            self.mtmt_mapping = MTMTMapping(
                self.__get_trustzones(),
                self.__get_components(),
                []
            )
        except Exception as e:
            raise LoadingMappingFileError('Error loading the mapping file. The mapping files are not valid.',
                                          e.__class__.__name__, str(e))

    def __get_trustzones(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.merged_mappings)
        return dict(zip([tz['label'] for tz in trustzone_mappings_list], trustzone_mappings_list))

    def __get_components(self):
        component_mappings_list = jmespath.search("components", self.merged_mappings)
        return dict(zip([tz['label'] for tz in component_mappings_list], component_mappings_list))

    def __merge_mapping(self):
        for mapping_data in self.provided_mappings:
            logger.info('Loading mapping data')
            data = mapping_data if isinstance(mapping_data, str) else mapping_data.decode()
            always_merger.merge(self.merged_mappings, yaml.load(data, Loader=yaml.BaseLoader))
            logger.debug('Mapping files loaded successfully')

    def get_mtmt_mapping(self):
        return self.mtmt_mapping
