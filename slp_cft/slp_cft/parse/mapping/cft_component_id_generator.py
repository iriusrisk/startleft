import sl_util.sl_util.secure_regex as re

VALID_ID_REGEX = r'\w+'


def normalize_name(name: str):
    return "_".join(re.findall(VALID_ID_REGEX, name.lower()))


def is_altsource_resource(source: dict) -> bool:
    return 'altsource' in source and source['altsource']


def build_path_id(id_elements: []):
    return ".".join(id_elements).rstrip('.')


# Check if additional data is needed to differentiate components generated from the same resource
def get_additional_id_data(source: dict, name: str) -> str:
    if 'SecurityGroup' in source['Type']:
        return name
    else:
        return ''


class CloudformationComponentIdGenerator:

    def __init__(self,
                 name: str,
                 parent_id: str,
                 type: str = None,
                 is_altsource: bool = False,
                 additional_id_data: str = ''):
        self.name = normalize_name(name)
        self.parent_id = parent_id
        self.type = type
        self.is_altsource = is_altsource
        self.additional_id_data = normalize_name(additional_id_data)

    @staticmethod
    def from_component(component_source: dict, parent_id: str, component_name: str = ''):
        is_altsource = is_altsource_resource(component_source)
        additional_id_data = get_additional_id_data(component_source, component_name)

        return CloudformationComponentIdGenerator(
            name=component_source['_key'],
            type=component_source['Type'],
            parent_id=parent_id,
            is_altsource=is_altsource,
            additional_id_data=additional_id_data
        )

    def generate_id(self):
        if self.is_altsource:
            return self.__generate_altsource_component_id()
        else:
            return self.__generate_regular_component_id()

    def __generate_regular_component_id(self):
        return build_path_id([self.parent_id, self.name, self.additional_id_data])

    def __generate_altsource_component_id(self):
        return self.__generate_regular_component_id() + '-altsource'
