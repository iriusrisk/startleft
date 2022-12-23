from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from otm.otm.entity.trustzone import OtmTrustzone


class DiagramTrustzoneMapper:

    def __init__(self, components: [DiagramComponent],  trustzone_mappings: dict):
        self.components = components
        self.trustzone_mappings = trustzone_mappings

    def to_otm(self) -> [OtmTrustzone]:
        return self.__map_to_otm(self.__filter_trustzones())

    def get_default_trustzone(self) -> OtmTrustzone:
        if self.trustzone_mappings:
            # at least the "Public Cloud" trustzone must be in the mapping file to be valid
            default_trustzone_mapping = self.trustzone_mappings['Public Cloud']
            return OtmTrustzone(default_trustzone_mapping['id'], default_trustzone_mapping['type'])

    def __filter_trustzones(self) -> [DiagramComponent]:
        return list(filter(
            lambda c: c.name in self.trustzone_mappings and not c.parent,
            self.components))

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [OtmTrustzone]:
        return list(map(self.__build_otm_trustzone, trustzones)) \
            if trustzones \
            else []

    def __build_otm_trustzone(self, trustzone: DiagramComponent) -> OtmTrustzone:
        trustzone_mapping = self.trustzone_mappings[trustzone.name]
        return OtmTrustzone(
            trustzone_id=trustzone_mapping['id'],
            name=trustzone_mapping['type']
        )
