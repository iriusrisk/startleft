from jsonschema._format import is_uuid

from otm.otm.otm import Dataflow
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT


class MTMTConnectorParser:

    def __init__(self, source: MTMT):
        self.source: MTMT = source

    def parse(self) -> [Dataflow]:
        dataflows = []
        for line in self.source.lines:
            if line.is_dataflow and self.__is_valid(line):
                dataflows.append(self.__create_dataflow(line))
        return dataflows

    @staticmethod
    def __create_dataflow(line: MTMLine) -> Dataflow:
        source_node_id = line.source_guid
        target_node_id = line.target_guid
        return Dataflow(id=line.id,
                        name=line.name,
                        properties=line.properties,
                        source_node=source_node_id,
                        destination_node=target_node_id,
                        bidirectional=False
                        )

    def __is_valid(self, line):
        return self.__is_valid_guid(line.source_guid) and self.__is_valid_guid(line.target_guid)

    @staticmethod
    def __is_valid_guid(guid):
        try:
            return guid and is_uuid(guid) and guid != '00000000-0000-0000-0000-000000000000'
        except ValueError:
            return False
