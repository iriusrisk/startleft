from otm.otm.entity.trustzone import OtmTrustzone
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.parse.mappers.diagram_mapper import DiagramMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator


def find_type(trustzone_mapping):
    if 'id' in trustzone_mapping:
        return trustzone_mapping['id']
    return trustzone_mapping['type']


class DiagramTrustzoneMapper(DiagramMapper):

    def __init__(self,
                 components: [DiagramComponent],
                 trustzone_mappings: dict,
                 representation_calculator: RepresentationCalculator):
        self.components = components
        self.trustzone_mappings = trustzone_mappings
        self.representation_calculator = representation_calculator

    def to_otm(self) -> [OtmTrustzone]:
        return self.__map_to_otm(self.__filter_trustzones())

    def __filter_trustzones(self) -> [DiagramComponent]:
        trustzones = []

        for c in self.components:
            if c.name in self.trustzone_mappings:
                c.trustzone = True
                trustzones.append(c)

        return trustzones

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [OtmTrustzone]:
        return list(map(self.__build_otm_trustzone, trustzones)) \
            if trustzones \
            else []

    def __build_otm_trustzone(self, trustzone: DiagramComponent) -> OtmTrustzone:
        trustzone_mapping = self.trustzone_mappings[trustzone.name]

        representation = self.representation_calculator.calculate_representation(trustzone)
        return OtmTrustzone(
            trustzone_id=trustzone.id,
            name=trustzone.name if trustzone.name else trustzone_mapping['type'],
            parent=self.__calculate_parent_id(trustzone),
            parent_type=self._calculate_parent_type(trustzone),
            type=find_type(trustzone_mapping),
            representations=[representation] if representation else None
        )

    def __calculate_parent_id(self, component: DiagramComponent) -> str:
        if component.parent:
            return component.parent.id

    def _get_trustzone_mappings(self):
        return self.trustzone_mappings
