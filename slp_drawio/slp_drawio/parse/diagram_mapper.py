import re
from functools import singledispatch
from typing import List, Dict, Optional

from sl_util.sl_util.iterations_utils import remove_from_list
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramComponent, DiagramTrustZone

EMPTY_COMPONENT_MAPPING = {
    'type': 'CD-V2-EMPTY-COMPONENT',
    'name': 'Empty Component'
}


@singledispatch
def __match(mapping_label, component_label: str) -> bool:
    return component_label == mapping_label


@__match.register(list)
def __match_by_list(mapping_label: List[str], component_label: str) -> bool:
    return component_label in mapping_label


@__match.register(dict)
def __match_by_dict(mapping_label: dict, component_label: str) -> bool:
    return bool(re.match(mapping_label.get('$regex'), component_label))


def _find_mapping(label: str, mappings: List[Dict]) -> Optional[Dict]:
    if not label:
        return None

    for mapping in mappings:
        if __match(mapping['label'], label):
            return mapping
    return None


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
        representations=component.otm.representations,
        default=False,
        shape_type=component.shape_type,
        shape_parent_id=component.shape_parent_id
    )


def _get_component_name_from_type(shape_type: str, mapping: Dict) -> str:
    name = None
    if mapping.get('type') != EMPTY_COMPONENT_MAPPING['type'] and mapping.get('name'):
        name = mapping['name']
    elif shape_type:
        name = shape_type \
                .capitalize() \
                .replace('Aws.', 'AWS ') \
                .replace('_', ' ') \
                .replace('-', ' ') \
                .replace('/', ' ')

    if not name:
        return 'N/A'

    return f'_{name}' if len(name) == 1 else name

class DiagramMapper:
    def __init__(self, diagram: Diagram, mapping: DrawioMapping):
        self._diagram: Diagram = diagram
        self._mapping: DrawioMapping = mapping

    def map(self):
        if self._mapping.trustzones:
            self._add_default_trustzone()

        if self._diagram.components:
            self._map_components()

    def _add_default_trustzone(self):
        self._diagram.default_trustzone = _create_default_trustzone(
            next(filter(lambda tz: tz.get('default', False), self._mapping.trustzones), self._mapping.trustzones[0]))

    def _map_components(self):
        mappings = self.__merge_mappings()

        for component in self._diagram.components:
            mapping = \
                _find_mapping(component.otm.name, mappings) or \
                _find_mapping(component.shape_type, mappings) or \
                EMPTY_COMPONENT_MAPPING

            self.__update_component_data(component, mapping)

        remove_from_list(self._diagram.components,
                         filter_function=lambda c: c.otm.id in [tz.otm.id for tz in self._diagram.trustzones])

    def __merge_mappings(self) -> List[Dict]:
        trustzone_mappings = [{**m, 'trustzone': True} for m in self._mapping.trustzones]
        return trustzone_mappings + self._mapping.components

    def __update_component_data(self, component: DiagramComponent, mapping: Dict):
        component.otm.type = mapping['type']
        component.otm.add_tag(mapping.get('name', mapping.get('type')))
        if not component.otm.name:
            component.otm.name = _get_component_name_from_type(component.shape_type, mapping)
        if mapping.get('trustzone', False):
            self._diagram.trustzones.append(_create_trustzone_from_component(component))
