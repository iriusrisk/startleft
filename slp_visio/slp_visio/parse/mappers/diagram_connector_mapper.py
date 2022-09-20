import uuid

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from startleft.otm.otm import Dataflow


def build_otm_dataflow(diagram_connector: DiagramConnector) -> Dataflow:
    return Dataflow(
        id=diagram_connector.id,
        name=str(uuid.uuid4()),
        source_node=diagram_connector.from_id,
        destination_node=diagram_connector.to_id,
        bidirectional=diagram_connector.bidirectional if diagram_connector.bidirectional else None
    )


class DiagramConnectorMapper:
    def __init__(self, connectors: [DiagramConnector]):
        self.connectors = connectors

    def to_otm(self):
        return list(map(build_otm_dataflow, self.connectors))

