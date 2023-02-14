import jmespath
import yaml
from deepmerge import always_merger

from otm.otm.entity.trustzone import Trustzone
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_base import MappingLoader
from slp_base.slp_base.mapping_file_loader import MappingFileLoader
from slp_visio.slp_visio.util.visio import normalize_unique_id

PUBLIC_CLOUD_NAME = 'Public Cloud'
PUBLIC_CLOUD = Trustzone(trustzone_id=deterministic_uuid(PUBLIC_CLOUD_NAME), name=PUBLIC_CLOUD_NAME,
                         type='b61d6911-338d-46a8-9f39-8dcd24abfe91', attributes={"default": True})


def load_mappings(mapping_file):
    if isinstance(mapping_file, dict):
        return mapping_file
    else:
        if isinstance(mapping_file, str):
            with open(mapping_file, 'r') as f:
                return always_merger.merge(mapping_file, yaml.safe_load(f))
        else:
            return always_merger.merge(mapping_file, yaml.safe_load(mapping_file))


class VisioMappingFileLoader(MappingLoader):

    def __init__(self, mapping_files):
        self.component_mappings = None
        self.trustzone_mappings = None
        self.default_otm_trustzone = None
        mapping = MappingFileLoader(mapping_files).load()
        self.mappings = load_mappings(mapping)

    def load(self):
        self.default_otm_trustzone = self.__load_default_otm_trustzone()
        self.trustzone_mappings = self.__load_trustzone_mappings()
        self.component_mappings = self.__load_component_mappings()

    def get_all_labels(self) -> [str]:
        component_and_tz_mappings = self.mappings['components'] + self.mappings['trustzones']
        return [c['label'] for c in component_and_tz_mappings]

    def __load_default_otm_trustzone(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.mappings)
        default_trustzones = [v for v in trustzone_mappings_list if 'default' in v and v['default']]
        default_otm_trustzone = default_trustzones[-1] if len(default_trustzones) > 0 else None
        if default_otm_trustzone:
            name = default_otm_trustzone['label']
            return Trustzone(trustzone_id=deterministic_uuid(name), name=name, type=default_otm_trustzone['type'],
                             attributes={"default": True})
        else:
            return PUBLIC_CLOUD

    def __load_trustzone_mappings(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.mappings)
        return dict(zip([tz['label'] for tz in trustzone_mappings_list], trustzone_mappings_list))

    def __load_component_mappings(self):
        component_mappings_list = jmespath.search("components", self.mappings)
        return dict(zip([self.__get_component_identifier(cp) for cp in component_mappings_list],
                        component_mappings_list))

    def __get_component_identifier(self, component: dict) -> str:
        identifier = component.get('id', component['label'])
        return normalize_unique_id(identifier)

    def get_trustzone_mappings(self):
        return self.trustzone_mappings

    def get_default_otm_trustzone(self):
        return self.default_otm_trustzone

    def get_component_mappings(self):
        return self.component_mappings
