import uuid

from startleft.diagram.objects.diagram_objects import DiagramComponent, DiagramConnector
from startleft.otm.otm import Dataflow


def calculate_parent_category(component: DiagramComponent) -> str:
    return component.parent.get_component_category() if component.parent else 'trustZone'


def build_otm_dataflow(diagram_connector: DiagramConnector) -> Dataflow:
    return Dataflow(
        id=diagram_connector.id,
        name=str(uuid.uuid4()),
        source_node=diagram_connector.from_id,
        destination_node=diagram_connector.to_id
    )


class DiagramConnectorMapper:
    def __init__(self, connectors: [DiagramConnector]):
        self.connectors = connectors

    def to_otm(self):
        return list(map(build_otm_dataflow, self.connectors))

