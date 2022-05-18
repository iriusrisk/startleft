import uuid

import jmespath
import yaml
from deepmerge import always_merger

from startleft.diagram.objects.diagram_objects import Diagram, DiagramComponent
from startleft.otm_builder import OtmBuilder
from startleft.otm import Component, Dataflow, Trustzone
from startleft.diagram.util.diagram_pruner import DiagramPruner


def is_trustzone(component: DiagramComponent) -> bool:
    return component.get_component_category() == 'trustZone'


def load_mappings(mapping_file):
    if isinstance(mapping_file, dict):
        return mapping_file
    else:
        if isinstance(mapping_file, str):
            with open(mapping_file, 'r') as f:
                return always_merger.merge(mapping_file, yaml.load(f, Loader=yaml.BaseLoader))
        else:
            return always_merger.merge(mapping_file, yaml.load(mapping_file, Loader=yaml.BaseLoader))


def get_mapping_labels(mappings: dict) -> [str]:
    component_and_tz_mappings = mappings['components'] + mappings['trustzones']
    return [c['label'] for c in component_and_tz_mappings]


class DiagramToOtm:

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_file):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mappings = load_mappings(mapping_file)

    def run(self):
        self.__prune_diagram()
        return self.__build_otm()

    def __prune_diagram(self):
        DiagramPruner(self.diagram, get_mapping_labels(self.mappings)).run()

    def __build_otm(self):
        trustzones, components = self.map_to_trustzones_and_components()
        dataflows = self.map_to_dataflows()

        return OtmBuilder(self.project_id, self.project_name, self.get_default_trustzone()) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(dataflows) \
            .build()

    def map_to_trustzones_and_components(self):
        trustzones = []
        components = []

        for diagram_component in self.diagram.components:
            if not is_trustzone(diagram_component):
                components.append(self.get_component(diagram_component))
            else:
                trustzone = self.get_trustzone(diagram_component.name)
                trustzones.append(Trustzone(trustzone['id'], trustzone['type']))

        return trustzones, components

    def get_trustzone(self, label: str):
        trustzones = jmespath.search("trustzones[?(@.label=='" + label + "')]", self.mappings)

        if not trustzones:
            return self.get_default_trustzone()

        return trustzones[0]

    def get_component(self, diagram_component: DiagramComponent) -> Component:
        return Component(
            id=diagram_component.id,
            name=diagram_component.name,
            type=self.calculate_otm_type(diagram_component.name, diagram_component.type),
            parent=self.calculate_parent_id(diagram_component),
            parent_type=diagram_component.parent.get_component_category()
        )

    def calculate_otm_type(self, component_name: str, component_type: str):
        otm_type = self.find_mapped_component_by_label(component_name)

        if not otm_type:
            otm_type = self.find_mapped_component_by_label(component_type)

        return otm_type or 'empty-component'

    def find_mapped_component_by_label(self, label: str) -> str:
        components = jmespath.search("components[?(@.label=='" + label + "')]", self.mappings)

        if components:
            return components[0]['type']

    def calculate_parent_id(self, component: DiagramComponent) -> str:
        return self.get_trustzone(component.parent.name)['id'] \
            if is_trustzone(component.parent) else component.parent.id

    def get_default_trustzone(self):
        return jmespath.search("trustzones[?(@.label=='Public Cloud')]", self.mappings)[0]

    def map_to_dataflows(self) -> [Component]:
        dataflows = []
        for diagram_connector in self.diagram.connectors:
            dataflows.append(Dataflow(
                id=diagram_connector.id,
                name=str(uuid.uuid4()),
                source_node=diagram_connector.from_id,
                destination_node=diagram_connector.to_id
            ))

        return dataflows
