from otm.otm.otm import OTM
from otm.otm.otm_builder import OtmBuilder
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import EtmType
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
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
        self.trustzoneParser = MTMTTrustzoneParser(self.source, self.mtmt_mapping)
        self.component_parser = MTMTComponentParser(self.source, self.mtmt_mapping, self.trustzoneParser)

    def __get_mtmt_components(self):
        return self.component_parser.parse()

    def __get_mtmt_dataflows(self):
        return MTMTConnectorParser(self.source).parse()

    def __get_mtmt_trustzones(self) -> list:
        return self.trustzoneParser.parse()

    def build_otm(self) -> OTM:
        components = self.__get_mtmt_components()
        trustzones = self.__get_mtmt_trustzones()
        return OtmBuilder(self.project_id, self.project_name, EtmType.MTMT) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(self.__get_mtmt_dataflows()) \
            .build()
