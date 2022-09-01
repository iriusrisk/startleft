from slp_visio.slp_visio.objects.diagram_objects import DiagramComponent
from startleft.otm.otm import Trustzone


class DiagramTrustzoneMapper:

    def __init__(self, components: [DiagramComponent],  trustzone_mappings: dict):
        self.components = components
        self.trustzone_mappings = trustzone_mappings

    def to_otm(self) -> [Trustzone]:
        return self.__map_to_otm(self.__filter_trustzones())

    def get_default_trustzone(self) -> Trustzone:
        default_trustzone_mapping = self.trustzone_mappings['Public Cloud']
        return Trustzone(default_trustzone_mapping['id'], default_trustzone_mapping['type'])

    def __filter_trustzones(self) -> [DiagramComponent]:
        return list(filter(
            lambda c: c.name in self.trustzone_mappings and not c.parent,
            self.components))

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [Trustzone]:
        return list(map(self.__build_otm_trustzone, trustzones)) \
            if trustzones \
            else [self.get_default_trustzone()]

    def __build_otm_trustzone(self, trustzone: DiagramComponent) -> Trustzone:
        trustzone_mapping = self.trustzone_mappings[trustzone.name]
        return Trustzone(
            id=trustzone_mapping['id'],
            name=trustzone_mapping['type']
        )
