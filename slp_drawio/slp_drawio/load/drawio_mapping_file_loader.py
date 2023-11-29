import logging
from typing import List, Dict

from slp_base.slp_base.mapping_file_loader import MappingFileLoader

logger = logging.getLogger(__name__)


class DrawioMapping:
    def __init__(self, trustzones: List[Dict], components: List[Dict]):
        self.trustzones: List[Dict] = trustzones
        self.components: List[Dict] = components


class DrawioMappingFileLoader(MappingFileLoader):
    def __init__(self, mapping_data_list: List[bytes]):
        super(DrawioMappingFileLoader, self).__init__(mapping_data_list)

    def get_mappings(self) -> DrawioMapping:
        return DrawioMapping(self.map['trustzones'], self.map['components'])
