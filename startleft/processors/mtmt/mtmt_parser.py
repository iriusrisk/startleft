from startleft.otm.otm import OTM
from startleft.otm.otm_builder import OtmBuilder
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.base.provider_type import EtmType
from startleft.processors.mtmt.mtmt_entity import MTMT
from startleft.processors.mtmt.mtmt_mapping_file_loader import MTMTMapping
from startleft.processors.mtmt.parse.mtmt_component_parser import MTMTComponentParser
from startleft.processors.mtmt.parse.mtmt_connector_parser import MTMTConnectorParser
from startleft.processors.mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser


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
