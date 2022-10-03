from otm.otm.otm import Dataflow
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT


class MTMTConnectorParser:

    def __init__(self, source: MTMT):
        self.source: MTMT = source

    def parse(self) -> [Dataflow]:
        dataflows = []
        for line in self.source.lines:
            if line.is_dataflow:
                dataflows.append(self.__create_dataflow(line))
        return dataflows

    @staticmethod
    def __create_dataflow(line: MTMLine) -> Dataflow:
        return Dataflow(id=line.id,
                        name=line.name,
                        properties=line.properties,
                        source_node=line.source_guid,
                        destination_node=line.target_guid,
                        bidirectional=False
                        )
