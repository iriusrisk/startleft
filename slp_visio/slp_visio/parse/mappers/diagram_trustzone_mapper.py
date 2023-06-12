from typing import Dict

from otm.otm.entity.trustzone import Trustzone
from sl_util.sl_util.iterations_utils import remove_nones
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.parse.mappers.diagram_mapper import DiagramMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator
from slp_visio.slp_visio.util.visio import normalize_label


def _find_type(trustzone_mapping):
    if 'id' in trustzone_mapping:
        return trustzone_mapping['id']
    return trustzone_mapping['type']


def _calculate_parent_id(component: DiagramComponent) -> str:
    if component.parent:
        return component.parent.id


class DiagramTrustzoneMapper(DiagramMapper):

    def __init__(self,
                 components: [DiagramComponent],
                 trustzone_mappings: dict,
                 representation_calculator: RepresentationCalculator):
        self.components = components
        self.trustzone_mappings = {normalize_label(lb): value for (lb, value) in trustzone_mappings.items()}
        self.representation_calculator = representation_calculator

    def to_otm(self) -> [Trustzone]:
        return self.__map_to_otm(self.components)

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [Trustzone]:
        return remove_nones(list(map(self.__build_otm_trustzone, trustzones))) \
            if trustzones \
            else []

    def __build_otm_trustzone(self, component: DiagramComponent) -> Trustzone:
        trustzone_mapping = self.__get_trustzone_mapping(component)

        if trustzone_mapping:
            component.trustzone = True
            representation = self.representation_calculator.calculate_representation(component)

            return Trustzone(
                trustzone_id=component.id,
                name=component.name if component.name else trustzone_mapping['type'],
                parent=_calculate_parent_id(component),
                parent_type=self._calculate_parent_type(component),
                type=_find_type(trustzone_mapping),
                representations=[representation] if representation else None
            )

    def __get_trustzone_mapping(self, component: DiagramComponent) -> Dict:
        return self.trustzone_mappings.get(normalize_label(component.name), {}) \
            or self.trustzone_mappings.get(normalize_label(component.type), {}) \
            or self.trustzone_mappings.get(component.unique_id, {})

    def _get_trustzone_mappings(self):
        return self.trustzone_mappings
