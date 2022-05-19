from startleft.diagram.objects.diagram_objects import DiagramComponent
from startleft.otm.otm import Trustzone, Component


def calculate_parent_category(component: DiagramComponent) -> str:
    return component.parent.get_component_category() if component.parent else 'trustZone'


class DiagramComponentMapper:
    def __init__(self,
                 components: [DiagramComponent],
                 component_mappings: dict,
                 trustzone_mappings: dict,
                 default_trustzone: Trustzone):
        self.components = components
        self.component_mappings = component_mappings
        self.trustzone_mappings = trustzone_mappings
        self.default_trustzone = default_trustzone

    def to_otm(self):
        component_candidates = list(filter(
            lambda c: c.name in self.component_mappings or c.type in self.component_mappings,
            self.components))

        return list(map(self.__build_otm_component, component_candidates))

    def __build_otm_component(self, diagram_component: DiagramComponent) -> Component:
        return Component(
            id=diagram_component.id,
            name=diagram_component.name,
            type=self.__calculate_otm_type(diagram_component.name, diagram_component.type),
            parent=self.__calculate_parent_id(diagram_component),
            parent_type=calculate_parent_category(diagram_component)
        )

    def __calculate_otm_type(self, component_name: str, component_type: str):
        otm_type = self.__find_mapped_component_by_label(component_name)

        if not otm_type:
            otm_type = self.__find_mapped_component_by_label(component_type)

        return otm_type or 'empty-component'

    def __find_mapped_component_by_label(self, label: str) -> str:
        return self.component_mappings[label]['type'] if label in self.component_mappings else None

    def __calculate_parent_id(self, component: DiagramComponent) -> str:
        if not component.parent:
            return self.default_trustzone.id

        return self.trustzone_mappings[component.parent.name]['id'] \
            if component.parent.name in self.trustzone_mappings \
            else component.parent.id
