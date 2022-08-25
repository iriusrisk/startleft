from startleft.processors.base.mapping import MappingLoader
import logging

logger = logging.getLogger(__name__)


class MTMTMapping:

    def __init__(self, trustzones, components, dataflows):
        self.trustzones = trustzones
        self.components = components
        self.dataflows = dataflows


class MTMTMappingFileLoader(MappingLoader):

    def __init__(self, default_mapping_file: bytes, custom_mapping_file: bytes):
        self.default_mapping_file = default_mapping_file
        self.custom_mapping_file = custom_mapping_file
        self.mtmt_mapping = None

    def load(self):
        self.mtmt_mapping = MTMTMapping(
            self.__get_trustzones(),
            self.__get_components(),
            []
        )

    def get_mtmt_mapping(self):
        return self.mtmt_mapping

    def __get_trustzones(self):
        pass

    def __get_components(self):
        pass
