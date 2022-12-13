from otm.otm.entity.dataflow import OtmDataflow
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser


class MTMTConnectorParser:

    def __init__(self, source: MTMT, component_parser: MTMTComponentParser):
        self.source: MTMT = source
        self.component_parser = component_parser

    def parse(self) -> [OtmDataflow]:
        dataflows = []
        for line in self.source.lines:
            if line.is_dataflow:
                dataflows.append(self.__create_dataflow(line))
        return dataflows

    @staticmethod
    def __create_dataflow(line: MTMLine) -> OtmDataflow:
        source_node_id = line.source_guid
        target_node_id = line.target_guid
        return OtmDataflow(dataflow_id=line.id,
                           name=line.name,
                           properties=line.properties,
                           source_node=source_node_id,
                           destination_node=target_node_id,
                           bidirectional=False
                           )
