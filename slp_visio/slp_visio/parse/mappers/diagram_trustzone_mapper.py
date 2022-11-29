from otm.otm.otm import Trustzone
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent


def find_type(trustzone_mapping):
    if 'id' in trustzone_mapping:
        return trustzone_mapping['id']
    return trustzone_mapping['type']


class DiagramTrustzoneMapper:

    def __init__(self, components: [DiagramComponent], trustzone_mappings: dict):
        self.components = components
        self.trustzone_mappings = trustzone_mappings

    def to_otm(self) -> [Trustzone]:
        return self.__map_to_otm(self.__filter_trustzones())

    def __filter_trustzones(self) -> [DiagramComponent]:
        return list(filter(
            lambda c: c.name in self.trustzone_mappings and not c.parent,
            self.components))

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [Trustzone]:
        return list(map(self.__build_otm_trustzone, trustzones)) \
            if trustzones \
            else []

    def __build_otm_trustzone(self, trustzone: DiagramComponent) -> Trustzone:
        trustzone_mapping = self.trustzone_mappings[trustzone.name]
        return Trustzone(
            id=trustzone.id,
            name=trustzone.name,
            type=find_type(trustzone_mapping)
        )
