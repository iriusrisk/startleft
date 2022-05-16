import uuid

import jmespath
import yaml
from deepmerge import always_merger

from startleft.diagram.visio_objects import VisioComponent, VisioConnector, VisioDiagram
from startleft.otm import OTM, Component, Dataflow, Trustzone
from startleft.provider import Provider


def is_trustzone(component: VisioComponent) -> bool:
    return component.get_component_category() == 'trustZone'


def map_to_dataflows(visio_connectors: [VisioConnector]) -> [Component]:
    dataflows = []
    for visio_connector in visio_connectors:
        dataflows.append(Dataflow(
            id=visio_connector.id,
            name=str(uuid.uuid4()),
            source_node=visio_connector.from_id,
            destination_node=visio_connector.to_id
        ))

    return dataflows


class OtmBuilder:
    def __init__(self, visio_diagram: VisioDiagram, mapping_file):
        self.visio_diagram = visio_diagram
        self.mapping_file = {}
        self.__load_mapping_file(mapping_file)

    def __load_mapping_file(self, mapping_file):
        if isinstance(mapping_file, dict):
            self.mapping_file = mapping_file
        else:
            if isinstance(mapping_file, str):
                with open(mapping_file, 'r') as f:
                    always_merger.merge(self.mapping_file, yaml.load(f, Loader=yaml.BaseLoader))
            else:
                always_merger.merge(self.mapping_file, yaml.load(mapping_file, Loader=yaml.BaseLoader))

    def build(self, project_name: str, project_id: str):
        otm = self.init_otm(project_name, project_id)

        trustzones, components = self.map_to_trustzones_and_components(self.visio_diagram.components)

        otm.trustzones = trustzones
        otm.components = components
        otm.dataflows = map_to_dataflows(self.visio_diagram.connectors)

        return otm

    def init_otm(self, project_name: str, project_id: str) -> OTM:
        otm = OTM(project_name, project_id, Provider.VISIO)

        default_trustzone = self.get_default_trustzone()
        otm.add_trustzone(default_trustzone['id'], default_trustzone['type'])

        return otm

    def map_to_trustzones_and_components(self, visio_components: [VisioComponent]):
        trustzones = []
        components = []

        for visio_component in visio_components:
            if not is_trustzone(visio_component):
                components.append(self.get_component(visio_component))
            else:
                trustzone = self.get_trustzone(visio_component.name)
                trustzones.append(Trustzone(trustzone['id'], trustzone['type']))

        return trustzones, components

    def get_trustzone(self, label: str):
        trustzones = jmespath.search("trustzones[?(@.label=='" + label + "')]", self.mapping_file)

        if not trustzones:
            return self.get_default_trustzone()

        return trustzones[0]

    def get_component(self, visio_component: VisioComponent) -> Component:
        return Component(
            id=visio_component.id,
            name=visio_component.name,
            type=self.get_component_type(visio_component.type),
            parent=self.calculate_parent_id(visio_component),
            parent_type=visio_component.parent.get_component_category()
        )

    def get_component_type(self, label: str):
        components = jmespath.search("components[?(@.label=='" + label + "')]", self.mapping_file)

        if not components:
            return "empty_component"

        return components[0]['type']

    def calculate_parent_id(self, component: VisioComponent) -> str:
        return self.get_trustzone(component.parent.name)['id'] if is_trustzone(
            component.parent) else component.parent.id

    def get_default_trustzone(self):
        return jmespath.search("trustzones[?(@.label=='Public Cloud')]", self.mapping_file)[0]
