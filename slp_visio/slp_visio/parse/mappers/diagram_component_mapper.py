from typing import Dict

from otm.otm.entity.component import Component
from otm.otm.entity.trustzone import Trustzone
from slp_base import MappingFileNotValidError
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.parse.mappers.diagram_mapper import DiagramMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator


class DiagramComponentMapper(DiagramMapper):

    def __init__(self,
                 components: [DiagramComponent],
                 component_mappings: Dict[str, dict],
                 trustzone_mappings: Dict[str, dict],
                 default_trustzone: Trustzone,
                 representation_calculator: RepresentationCalculator):
        self.components: [DiagramComponent] = components
        self.component_mappings = component_mappings
        self.trustzone_mappings = trustzone_mappings
        self.default_trustzone = default_trustzone

        self.representation_calculator = representation_calculator

    def to_otm(self) -> [Component]:
        return self.__map_to_otm(self.components)

    def __map_to_otm(self, components: [DiagramComponent]) -> [Component]:
        otm_components = []

        for diag_component in components:
            component_mapping = self.component_mappings.get(diag_component.id, None)
            if component_mapping:
                otm_components.append(
                    self.__build_otm_component(diag_component, component_mapping.get('type'))
                )
                
        return otm_components

    def __build_otm_component(self, diagram_component: DiagramComponent, otm_type: str) -> Component:
        representation = self.representation_calculator.calculate_representation(diagram_component)

        return Component(
            component_id=diagram_component.id,
            name=diagram_component.name,
            component_type=otm_type,
            parent=self.__calculate_parent_id(diagram_component),
            parent_type=self._calculate_parent_type(diagram_component),
            representations=[representation] if representation else None
        )

    def __calculate_parent_id(self, component: DiagramComponent) -> str:
        if component.parent:
            return component.parent.id

        if self.default_trustzone:
            return self.default_trustzone.id

        raise MappingFileNotValidError('Mapping files are not valid',
                                       'No default trust zone has been defined in the mapping file',
                                       'Please, add a default trust zone')

    def _get_trustzone_mappings(self):
        return self.trustzone_mappings
