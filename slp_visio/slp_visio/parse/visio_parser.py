import re
from functools import singledispatch
from typing import List, Dict

from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from otm.otm.entity.trustzone import Trustzone
from otm.otm.otm_builder import OTMBuilder
from otm.otm.otm_pruner import OTMPruner
from slp_base import ProviderParser
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponent
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator, \
    build_size_object, calculate_diagram_size
from slp_visio.slp_visio.util.visio import normalize_unique_id, normalize_label


def _match_resource_by_unique_id(resource_unique_id: str, resource: DiagramComponent) -> bool:
    resource_unique_id = normalize_unique_id(resource_unique_id)
    return resource_unique_id == resource.unique_id


@singledispatch
def _match_resource(label, value: str) -> bool:
    return normalize_label(label) == normalize_label(value)


@_match_resource.register(list)
def _match_resource_by_list(labels: List[str], value: str) -> bool:
    for label in labels:
        if _match_resource(label, value):
            return True


@_match_resource.register(dict)
def _match_resource_by_dict(label: dict, value: str) -> bool:
    if '$regex' in label:
        if re.match(label.get('$regex'), value) \
                or re.match(label.get('$regex'), normalize_label(value)):
            return True


def _get_diagram_component_mapping_by_id(resource: DiagramComponent, mappings: [dict]) -> dict:
    for mapping in mappings:
        if 'id' in mapping and _match_resource_by_unique_id(mapping.get('id'), resource):
            return mapping


def _get_diagram_component_mapping_by_name(resource: DiagramComponent, mappings: [dict]) -> dict:
    for mapping in mappings:
        if _match_resource(mapping.get('label'), resource.name):
            return mapping


def _get_diagram_component_mapping_by_type(resource: DiagramComponent, mappings: [dict]) -> dict:
    for mapping in mappings:
        if _match_resource(mapping.get('label'), resource.type):
            return mapping


def _get_diagram_component_mapping(resource: DiagramComponent, mappings: [dict]) -> dict:
    """
    Returns the mapping for the given resource. The mapping is determined by the following order:
    1. id
    2. name
    3. type
    :param resource:
    :param mappings:
    :return:
    """
    return _get_diagram_component_mapping_by_id(resource, mappings) or \
        _get_diagram_component_mapping_by_name(resource, mappings) or \
        _get_diagram_component_mapping_by_type(resource, mappings)


class VisioParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = mapping_loader

        self.representation_id = f'{self.project_id}-diagram'
        self.representations = [
            DiagramRepresentation(
                id_=self.representation_id,
                name=f'{self.project_id} Diagram Representation',
                type_=RepresentationType.DIAGRAM,
                size=build_size_object(calculate_diagram_size(self.diagram.limits))
            )
        ]

        self._representation_calculator = RepresentationCalculator(self.representation_id, self.diagram.limits)
        self.__default_trustzone = self.mapping_loader.get_default_otm_trustzone()
        self.__trustzone_mappings = {}
        self.__component_mappings = {}

    def build_otm(self):
        self.__trustzone_mappings = self._get_trustzone_mappings()
        self.__component_mappings = self._get_component_mappings()

        self.__prune_diagram()

        components = self.__map_components()
        trustzones = self.__map_trustzones()
        dataflows = self.__map_dataflows()

        otm = self.__build_otm(trustzones, components, dataflows)
        OTMPruner(otm).prune_orphan_dataflows()

        return otm

    def _get_trustzone_mappings(self) -> Dict[str, dict]:
        return self.__get_shape_mappings(self.mapping_loader.get_trustzone_mappings())

    def _get_component_mappings(self) -> Dict[str, dict]:
        return self.__get_shape_mappings(self.mapping_loader.get_component_mappings())

    def __get_shape_mappings(self, mappings: [dict]) -> Dict[str, dict]:
        result = {}
        for diag_component in self.diagram.components:
            mapping = _get_diagram_component_mapping(diag_component, mappings)
            if mapping:
                result[diag_component.id] = mapping
        return result

    def __get_all_key_mappings(self) -> List[str]:
        return list(self.__trustzone_mappings.keys()) + list(self.__component_mappings.keys())

    def __prune_diagram(self):
        DiagramPruner(self.diagram, self.__get_all_key_mappings()).run()

    def __map_trustzones(self):
        trustzone_mapper = DiagramTrustzoneMapper(
            self.diagram.components,
            self.__trustzone_mappings,
            self._representation_calculator
        )
        return trustzone_mapper.to_otm()

    def __map_components(self):
        return DiagramComponentMapper(
            self.diagram.components,
            self.__component_mappings,
            self.__trustzone_mappings,
            self.__default_trustzone,
            self._representation_calculator,
        ).to_otm()

    def __map_dataflows(self):
        return DiagramConnectorMapper(self.diagram.connectors).to_otm()

    def __build_otm(self, trustzones: [Trustzone], components: [Component], dataflows: [Dataflow]):
        otm_builder = OTMBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_representations(self.representations, extend=False) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(dataflows)

        if self.__default_trustzone and self.__any_default_tz(components):
            otm_builder.add_default_trustzone(self.__default_trustzone)

        return otm_builder.build()

    def __any_default_tz(self, components):
        for component in components:
            if self.__default_trustzone and component.parent \
                    and component.parent == self.__default_trustzone.id:
                return True
        return False
