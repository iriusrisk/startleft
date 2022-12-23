from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from otm.otm.entity.component import OtmComponent
from otm.otm.entity.trustzone import OtmTrustzone
from slp_visio.slp_visio.util.visio import normalize_label


class DiagramComponentMapper:
    def __init__(self,
                 components: [DiagramComponent],
                 component_mappings: dict,
                 trustzone_mappings: dict,
                 default_trustzone: OtmTrustzone):
        self.components = components
        self.normalized_component_mappings = {normalize_label(lb): value for (lb, value) in component_mappings.items()}
        self.trustzone_mappings = trustzone_mappings
        self.default_trustzone = default_trustzone

    def to_otm(self) -> [OtmComponent]:
        return self.__map_to_otm(self.__filter_components())

    def __filter_components(self) -> [DiagramComponent]:
        return [component for component in self.components if self.__filter_component(component)]

    def __filter_component(self, component):
        map_by_name = normalize_label(component.name) in self.normalized_component_mappings
        map_by_type = normalize_label(component.type) in self.normalized_component_mappings
        return map_by_name or map_by_type

    def __map_to_otm(self, component_candidates: [DiagramComponent]) -> [OtmComponent]:
        return list(map(self.__build_otm_component, component_candidates))

    def __build_otm_component(self, diagram_component: DiagramComponent) -> OtmComponent:
        return OtmComponent(
            component_id=diagram_component.id,
            name=diagram_component.name,
            component_type=self.__calculate_otm_type(diagram_component.name, diagram_component.type),
            parent=self.__calculate_parent_id(diagram_component),
            parent_type=self.__calculate_parent_type(diagram_component)
        )

    def __calculate_otm_type(self, component_name: str, component_type: str) -> str:
        otm_type = self.__find_mapped_component_by_label(component_name)

        if not otm_type:
            otm_type = self.__find_mapped_component_by_label(component_type)

        return otm_type or 'empty-component'

    def __find_mapped_component_by_label(self, label: str) -> str:
        normalized_label = normalize_label(label)
        return self.normalized_component_mappings[normalized_label]['type']\
            if normalized_label in self.normalized_component_mappings else None

    def __calculate_parent_id(self, component: DiagramComponent) -> str:
        if not component.parent:
            return self.default_trustzone.id if self.default_trustzone else None

        return self.trustzone_mappings[component.parent.name]['id'] \
            if component.parent.name in self.trustzone_mappings \
            else component.parent.id

    def __calculate_parent_type(self, component: DiagramComponent) -> str:
        if not component.parent or component.parent.name in self.trustzone_mappings.keys():
            return 'trustZone'
        else:
            return 'component'
