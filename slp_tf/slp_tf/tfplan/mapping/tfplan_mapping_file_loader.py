from slp_base.slp_base.mapping_file_loader import MappingFileLoader
from slp_base import MappingFileNotValidError


def simple_type(component: {}) -> []:
    terraform_types = component['$source']['$type']
    if type(terraform_types) == str:
        terraform_types = [terraform_types]

    return list(map(lambda tf_type: {
        'otm_type': component['type'],
        'tf_type': tf_type
    }, terraform_types))


def simple_regex(component: {}) -> []:
    return [{
        'otm_type': component['type'],
        'tf_type': {'$regex': component['$source']['$type']['$regex']}
    }]


def simple_singleton(component: {}) -> []:
    return [{
        'otm_type': component['type'],
        'tf_type': component['$source']['$singleton']['$type'],
        'singleton': True
    }]


def regex_singleton(component: {}) -> []:
    return [{
        'otm_type': component['type'],
        'tf_type': {'$regex': component['$source']['$singleton']['$type']['$regex']},
        'singleton': True
    }]


def get_source_structure(source: {}, structure: list) -> []:
    for key, value in source.items():
        structure.append(key)
        if type(value) == dict:
            get_source_structure(value, structure)

    return structure


SOURCE_STRUCTURES = {
    tuple(['$type']): simple_type,
    ('$type', '$regex'): simple_regex,
    ('$singleton', '$type'): simple_singleton,
    ('$singleton', '$type', '$regex'): regex_singleton,
}


class TfplanMappingFileLoader(MappingFileLoader):

    def __init__(self, mapping_files_data: [bytes]):
        super().__init__(mapping_files_data)

    def load(self):
        super().load()
        self.__read_default_trustzone()
        self.__transform_component_mappings()
        self.__remove_dataflows()

    def __transform_component_mappings(self):
        flat_components = []

        for component in self.map['components']:
            source_structure = tuple(get_source_structure(component['$source'], []))
            if source_structure in SOURCE_STRUCTURES:
                flat_components.extend(SOURCE_STRUCTURES[source_structure](component))

        self.map['components'] = flat_components

    def __read_default_trustzone(self):
        default_trustzone = list(filter(
            lambda tz: '$default' in tz and tz['$default'] == 'true', self.map['trustzones']))

        if not default_trustzone:
            msg = 'Mapping file must contain a default TrustZone'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

        self.map['default_trustzone'] = default_trustzone[0]
        del self.map['trustzones']

    def __remove_dataflows(self):
        self.map.pop('dataflows', None)
