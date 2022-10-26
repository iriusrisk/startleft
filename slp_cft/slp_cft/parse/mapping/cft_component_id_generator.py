import re

VALID_ID_REGEX = r"(\w+)"


def normalize_name(name: str):
    return "_".join(re.findall(VALID_ID_REGEX, name.lower()))


def is_altsource_resource(source: dict) -> bool:
    return 'altsource' in source and source['altsource']


def build_path_id(id_elements: []):
    return ".".join(id_elements)


class CloudformationComponentIdGenerator:

    def __init__(self,
                 name: str,
                 parent_id: str,
                 type: str = None,
                 is_altsource: bool = False):
        self.name = normalize_name(name)
        self.parent_id = parent_id
        self.type = type
        self.is_altsource = is_altsource

    @staticmethod
    def from_component(component_source: dict, parent_id: str):
        is_altsource = is_altsource_resource(component_source)

        return CloudformationComponentIdGenerator(
            name=component_source['_key'],
            type=component_source['Type'],
            parent_id=parent_id,
            is_altsource=is_altsource
        )

    def generate_id(self):
        if self.is_altsource:
            return self.__generate_altsource_component_id()
        else:
            return self.__generate_regular_component_id()

    def __generate_regular_component_id(self):
        return build_path_id([self.parent_id, self.name])

    def __generate_altsource_component_id(self):
        return self.__generate_regular_component_id() + '-altsource'
