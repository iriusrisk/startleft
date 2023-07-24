from typing import Dict

from otm.otm.entity.trustzone import Trustzone
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.parse.mappers.diagram_mapper import DiagramMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator


def _find_type(tz_mapping):
    if 'id' in tz_mapping:
        return tz_mapping['id']
    return tz_mapping['type']


def _calculate_parent_id(component: DiagramComponent) -> str:
    if component.parent:
        return component.parent.id


class DiagramTrustzoneMapper(DiagramMapper):

    def __init__(self,
                 trustzones: [DiagramComponent],
                 trustzone_mappings: Dict[str, dict],
                 representation_calculator: RepresentationCalculator):
        self.trustzones = trustzones
        self.trustzone_mappings = trustzone_mappings
        self.representation_calculator = representation_calculator

    def to_otm(self) -> [Trustzone]:
        return self.__map_to_otm(self.trustzones)

    def __map_to_otm(self, trustzones: [DiagramComponent]) -> [Trustzone]:
        otm_trustzones = []

        for diag_tz in trustzones:
            tz_mapping = self.trustzone_mappings.get(diag_tz.id, None)
            if tz_mapping:
                otm_trustzones.append(self.__build_otm_trustzone(diag_tz, tz_mapping))
        return otm_trustzones

    def __build_otm_trustzone(self, diag_tz: DiagramComponent, tz_mapping: dict) -> Trustzone:
        diag_tz.trustzone = True
        representation = self.representation_calculator.calculate_representation(diag_tz)

        return Trustzone(
            trustzone_id=diag_tz.id,
            name=diag_tz.name if diag_tz.name else tz_mapping['type'],
            parent=_calculate_parent_id(diag_tz),
            parent_type=self._calculate_parent_type(diag_tz),
            type=_find_type(tz_mapping),
            representations=[representation] if representation else None
        )

    def _get_trustzone_mappings(self):
        return self.trustzone_mappings
