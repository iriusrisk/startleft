import uuid

from startleft.provider import Provider
from startleft.diagram.otm_mappings_and_defaults import *
from startleft.otm import OTM, Component, Dataflow
from startleft.diagram.visio_objects import VisioComponent, VisioConnector, VisioDiagram


def init_otm() -> OTM:
    otm = OTM(OTM_DEFAULT_NAME, OTM_DEFAULT_ID, Provider.VISIO)
    otm.add_trustzone(DEFAULT_TRUSTZONE.id, DEFAULT_TRUSTZONE.name)

    return otm


def map_to_trustzones_and_components(visio_components: [VisioComponent]):
    trustzones = []
    components = []

    for visio_component in visio_components:
        if not is_trustzone(visio_component):
            components.append(get_component(visio_component))
        else:
            trustzone = get_trustzone_by_name(visio_component)
            trustzones.append(Trustzone(trustzone.id, trustzone.name))

    return trustzones, components


def get_component(visio_component: VisioComponent) -> Component:
    return Component(
        id=visio_component.id,
        name=visio_component.name,
        type=get_component_by_visio_type(visio_component.type),
        parent=calculate_parent_id(visio_component),
        parent_type=visio_component.parent.get_component_category()
    )


def get_component_by_visio_type(visio_type: str):
    return MAPPING_VISIO_OTM_COMPONENTS.get(visio_type) or DEFAULT_COMPONENT_TYPE


def calculate_parent_id(component: VisioComponent) -> str:
    return get_trustzone_by_name(component.parent).id if is_trustzone(component.parent) else component.parent.id


def is_trustzone(component: VisioComponent) -> bool:
    return component.get_component_category() == 'trustZone'


def get_trustzone_by_name(trustzone: VisioComponent) -> Trustzone:
    return MAPPING_VISIO_OTM_TRUSTZONES.get(trustzone.name) or DEFAULT_TRUSTZONE


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
    def __init__(self, visio_diagram: VisioDiagram):
        self.visio_diagram = visio_diagram

    def build(self):
        otm = init_otm()

        trustzones, components = map_to_trustzones_and_components(self.visio_diagram.components)

        otm.trustzones = trustzones
        otm.components = components
        otm.dataflows = map_to_dataflows(self.visio_diagram.connectors)

        return otm
