import logging
from typing import List, Dict

import yaml

from slp_base.slp_base.mapping_file_loader import MappingFileLoader

logger = logging.getLogger(__name__)


class AbacusMapping:
    def __init__(self, trustzones: List[Dict], components: List[Dict]):
        self.trustzones: List[Dict] = trustzones
        self.components: List[Dict] = components

    @classmethod
    def from_yaml(cls, yaml_content: str):
        yaml_data = yaml.safe_load(yaml_content)
        trustzones = yaml_data.get('trustzones', [])
        components = yaml_data.get('components', [])
        return cls(trustzones, components)


class AbacusMappingFileLoader(MappingFileLoader):

    def __init__(self, mapping_data_list: List[bytes]):
        super(AbacusMappingFileLoader, self).__init__(mapping_data_list)

    def get_mappings(self) -> AbacusMapping:
        return AbacusMapping(self.map['trustzones'], self.map['components'])
