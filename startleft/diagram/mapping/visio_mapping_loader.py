import jmespath
import yaml
from deepmerge import always_merger


def load_mappings(mapping_file):
    if isinstance(mapping_file, dict):
        return mapping_file
    else:
        if isinstance(mapping_file, str):
            with open(mapping_file, 'r') as f:
                return always_merger.merge(mapping_file, yaml.load(f, Loader=yaml.BaseLoader))
        else:
            return always_merger.merge(mapping_file, yaml.load(mapping_file, Loader=yaml.BaseLoader))


class DiagramMappingLoader:
    def __init__(self, mapping_file):
        self.mappings = load_mappings(mapping_file)

    def load_mappings(self):
        return self.__get_trustzone_mappings(), self.__get_component_mappings()

    def get_all_labels(self) -> [str]:
        component_and_tz_mappings = self.mappings['components'] + self.mappings['trustzones']
        return [c['label'] for c in component_and_tz_mappings]

    def __get_trustzone_mappings(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.mappings)
        return dict(zip([tz['label'] for tz in trustzone_mappings_list], trustzone_mappings_list))

    def __get_component_mappings(self):
        component_mappings_list = jmespath.search("components", self.mappings)
        return dict(zip([tz['label'] for tz in component_mappings_list], component_mappings_list))
