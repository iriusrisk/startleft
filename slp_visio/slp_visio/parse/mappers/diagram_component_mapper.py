from otm.otm.otm import Component, Trustzone
from slp_base import MappingFileNotValidError
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent


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

    def to_otm(self) -> [Component]:
        return self.__map_to_otm(self.__filter_components())

    def __filter_components(self) -> [DiagramComponent]:
        return list(filter(
            lambda c: c.name in self.component_mappings or c.type in self.component_mappings,
            self.components))

    def __map_to_otm(self, component_candidates: [DiagramComponent]) -> [Component]:
        return list(map(self.__build_otm_component, component_candidates))

    def __build_otm_component(self, diagram_component: DiagramComponent) -> Component:
        return Component(
            id=diagram_component.id,
            name=diagram_component.name,
            type=self.__calculate_otm_type(diagram_component.name, diagram_component.type),
            parent=self.__calculate_parent_id(diagram_component),
            parent_type=self.__calculate_parent_type(diagram_component)
        )

    def __calculate_otm_type(self, component_name: str, component_type: str) -> str:
        otm_type = self.__find_mapped_component_by_label(component_name)

        if not otm_type:
            otm_type = self.__find_mapped_component_by_label(component_type)

        return otm_type or 'empty-component'

    def __find_mapped_component_by_label(self, label: str) -> str:
        return self.component_mappings[label]['type'] if label in self.component_mappings else None

    def __calculate_parent_id(self, component: DiagramComponent) -> str:
        if component.parent:
            return component.parent.id

        if self.default_trustzone:
            return self.default_trustzone.id

        raise MappingFileNotValidError('Mapping files are not valid',
                                       'No default trust zone has been defined in the mapping file',
                                       'Please, add a default trust zone')

    def __calculate_parent_type(self, component: DiagramComponent) -> str:
        if not component.parent or component.parent.name in self.trustzone_mappings.keys():
            return 'trustZone'
        else:
            return 'component'
