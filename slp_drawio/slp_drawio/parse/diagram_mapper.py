import re
from functools import singledispatch
from typing import List, Dict

from sl_util.sl_util.iterations_utils import remove_from_list
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramComponent, DiagramTrustZone

DEFAULT_COMPONENT_TYPE = 'empty-component'


@singledispatch
def __match(mapping_label, component_label: str) -> bool:
    return component_label == mapping_label


@__match.register(list)
def __match_by_list(label: List[str], component_identifier: str) -> bool:
    return component_identifier in label


@__match.register(dict)
def __match_by_dict(label: dict, component_identifier: str) -> bool:
    return bool(re.match(label.get('$regex'), component_identifier))


def _find_mapping(label: str, mappings: List[Dict]) -> Dict:
    return next(filter(lambda m: __match(m['label'], label), mappings), None)


def _create_default_trustzone(trustzone_mapping: Dict) -> DiagramTrustZone:
    return DiagramTrustZone(
        type_=trustzone_mapping['type'],
        id_=deterministic_uuid(f'default-{trustzone_mapping["type"]}'),
        name=trustzone_mapping.get('label', trustzone_mapping['type']),
        default=True
    )


def _create_trustzone_from_component(component: DiagramComponent) -> DiagramTrustZone:
    return DiagramTrustZone(
        type_=component.otm.type,
        id_=component.otm.id,
        name=component.otm.name,
        default=False,
        shape_type=component.shape_type,
        shape_parent_id=component.shape_parent_id
    )


class DiagramMapper:
    def __init__(self, diagram: Diagram, mapping: DrawioMapping):
        self._diagram: Diagram = diagram
        self._mapping: DrawioMapping = mapping

    def map(self):
        if self._mapping.trustzones:
            self._add_default_trustzone()

        if self._diagram.components:
            self._map_components()
            self._set_default_type_to_unmapped_components()

    def _add_default_trustzone(self):
        default_trustzone_mapping = next(filter(lambda tz: tz.get('default', False), self._mapping.trustzones),
                                         self._mapping.trustzones[0])
        if default_trustzone_mapping:
            self._diagram.default_trustzone = _create_default_trustzone(default_trustzone_mapping)

    def _map_components(self):
        mappings = self.__merge_mappings()
        new_trustzones = []

        for component in self._diagram.components:
            mapping = _find_mapping(component.otm.name, mappings) or _find_mapping(component.shape_type, mappings)
            if mapping:
                self.__change_component_type(component, mapping, new_trustzones)

        remove_from_list(self._diagram.components, filter_function=lambda c: c in new_trustzones)

    def _set_default_type_to_unmapped_components(self):
        for component in self._diagram.components:
            if not component.otm.type:
                component.otm.type = DEFAULT_COMPONENT_TYPE

    def __merge_mappings(self) -> List[Dict]:
        trustzone_mappings = [{**m, 'trustzone': True} for m in self._mapping.trustzones]
        return trustzone_mappings + self._mapping.components

    def __change_component_type(self, component: DiagramComponent, mapping: Dict, new_trustzones: List):
        component.otm.type = mapping['type']
        if mapping.get('trustzone', False):
            self._diagram.trustzones.append(_create_trustzone_from_component(component))
            new_trustzones.append(component)
