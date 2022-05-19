from startleft.diagram.objects.diagram_objects import DiagramComponent
from startleft.otm.otm import Trustzone


class DiagramTrustzoneMapper:

    def __init__(self, components: [DiagramComponent],  trustzone_mappings: dict):
        self.components = components
        self.trustzone_mappings = trustzone_mappings

    def to_otm(self):
        trustzone_candidates = list(filter(
            lambda c: c.name in self.trustzone_mappings and not c.parent,
            self.components))

        return list(map(self.__build_otm_trustzone, trustzone_candidates)) \
            if trustzone_candidates \
            else [self.get_default_trustzone()]

    def get_default_trustzone(self):
        default_trustzone_mapping = self.trustzone_mappings['Public Cloud']
        return Trustzone(default_trustzone_mapping['id'], default_trustzone_mapping['type'])

    def __build_otm_trustzone(self, trustzone: DiagramComponent) -> Trustzone:
        trustzone_mapping = self.trustzone_mappings[trustzone.name]
        return Trustzone(
            id=trustzone_mapping['id'],
            name=trustzone_mapping['type']
        )
