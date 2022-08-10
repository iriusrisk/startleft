from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.mtmt.mtmt_entity import MTMT
from startleft.otm.otm import OTM
from startleft.processors.base.provider_type import EtmType
from startleft.otm.otm_builder import OtmBuilder
from startleft.processors.mtmt.parse.mtmt_component_parser import MtmtComponentParser
from startleft.processors.mtmt.parse.mtmt_connector_parser import MtmtConnectorParser
from startleft.processors.mtmt.parse.mtmt_trustzone_parser import MtmtTrustzoneParser


class MTMTParser(ProviderParser):
    """
    Parser to build an OTM from Microsoft Threat Model
    """

    def __init__(self, source: MTMT, mapping: [str]):
        self.source = source
        self.mapping = mapping

    def __get_mtmt_components(self):
        return MtmtComponentParser().parse()

    def __get_mtmt_dataflows(self):
        return MtmtConnectorParser().parse()

    def __get_mtmt_trustzones(self) -> list:
        return MtmtTrustzoneParser().parse()

    def __get_mtmt_default_trustzones(self):
        return MtmtTrustzoneParser().parse_default_trustzone()

    def build_otm(self, project_id: str, project_name: str) -> OTM:
        return OtmBuilder(project_id, project_name, EtmType.MTMT) \
            .add_default_trustzone(self.__get_mtmt_default_trustzones()) \
            .add_trustzones(self.__get_mtmt_trustzones()) \
            .add_components(self.__get_mtmt_components()) \
            .add_dataflows(self.__get_mtmt_dataflows()) \
            .build()
