from otm.otm.entity.component import Component
from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from otm.otm.otm_builder import OTMBuilder

from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import EtmType
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.parse.mtmt_component_parser import MTMTComponentParser
from slp_mtmt.slp_mtmt.parse.mtmt_connector_parser import MTMTConnectorParser
from slp_mtmt.slp_mtmt.parse.mtmt_threat_parser import MTMThreatParser
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from otm.otm.trustzone_representation_calculator import calculate_missing_trustzones_representations


class MTMTParser(ProviderParser):
    """
    Parser to build an OTM from Microsoft Threat Model
    """

    def __init__(self, project_id: str, project_name: str, source: MTMT, mtmt_mapping: MTMTMapping):
        self.source = source
        self.mtmt_mapping = mtmt_mapping
        self.project_id = project_id
        self.project_name = project_name
        self.representations = [
            DiagramRepresentation(
                id_=f'{self.project_id}-diagram',
                name=f'{self.project_id} Diagram Representation',
                type_=RepresentationType.DIAGRAM,
                size={'width': 2000, 'height': 2000}
            )
        ]

        self.trustzone_parser = MTMTTrustzoneParser(self.source, self.mtmt_mapping, self.representations[0].id)
        self.component_parser = MTMTComponentParser(
            self.source,
            self.mtmt_mapping,
            self.trustzone_parser,
            self.representations[0].id
        )
        self.threat_parser = MTMThreatParser(self.source)

        self.trustzones = self.trustzone_parser.parse()
        self.components = self.component_parser.parse()
        self.dataflows = MTMTConnectorParser(self.source).parse()

    def __get_mtmt_components(self):
        return self.components

    def __get_mtmt_dataflows(self):
        return self.dataflows

    def __get_mtmt_trustzones(self) -> list:
        return self.trustzones

    def __get_mtmt_threats_and_mitigations(self, components: [Component]):
        return self.threat_parser.parse(components)

    def __get_mtmt_representations(self) -> list:
        return self.representations

    def build_otm(self) -> OTM:
        threats, mitigations = self.__get_mtmt_threats_and_mitigations(self.__get_mtmt_components())
        otm_representations = self.__get_mtmt_representations()

        otm = OTMBuilder(self.project_id, self.project_name, EtmType.MTMT) \
            .add_representations(otm_representations) \
            .add_trustzones(self.__get_mtmt_trustzones()) \
            .add_components(self.__get_mtmt_components()) \
            .add_dataflows(self.__get_mtmt_dataflows()) \
            .add_threats(threats) \
            .add_mitigations(mitigations) \
            .build()

        calculate_missing_trustzones_representations(otm, otm_representations[0].id)

        return otm
