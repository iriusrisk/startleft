from otm.otm.otm import OTM
from otm.otm.otm_builder import OtmBuilder
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import EtmType
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser
from slp_mtmt.slp_mtmt.parse.mtmt_connector_parser import MTMTConnectorParser
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser


class MTMTParser(ProviderParser):
    """
    Parser to build an OTM from Microsoft Threat Model
    """

    def __init__(self, project_id: str, project_name: str, source: MTMT, mtmt_mapping: MTMTMapping):
        self.source = source
        self.mtmt_mapping = mtmt_mapping
        self.project_id = project_id
        self.project_name = project_name

    def __get_mtmt_components(self):
        return MTMTComponentParser(self.source, self.mtmt_mapping).parse()

    def __get_mtmt_dataflows(self):
        return MTMTConnectorParser().parse()

    def __get_mtmt_trustzones(self) -> list:
        return MTMTTrustzoneParser().parse()

    def __get_mtmt_default_trustzones(self):
        return MTMTTrustzoneParser().parse_default_trustzone()

    def build_otm(self) -> OTM:
        return OtmBuilder(self.project_id, self.project_name, EtmType.MTMT) \
            .add_default_trustzone(self.__get_mtmt_default_trustzones()) \
            .add_trustzones(self.__get_mtmt_trustzones()) \
            .add_components(self.__get_mtmt_components()) \
            .add_dataflows(self.__get_mtmt_dataflows()) \
            .build()
