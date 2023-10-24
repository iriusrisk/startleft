from otm.otm.entity.otm import OTM
from otm.otm.otm_builder import OTMBuilder

from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import DiagramType
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram
from slp_drawio.slp_drawio.parse.diagram_mapper import DiagramMapper
from slp_drawio.slp_drawio.parse.tranformers.parent_calculator_transformer import ParentCalculatorTransformer
from slp_drawio.slp_drawio.parse.transformer.default_trustzone_transformer import DefaultTrustZoneTransformer


class DrawioParser(ProviderParser):
    """
    Parser to build an OTM from DrawIO
    """

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping: DrawioMapping):
        self.diagram = diagram
        self.mapping = mapping
        self.project_id = project_id
        self.project_name = project_name

    def build_otm(self) -> OTM:
        DiagramMapper(self.diagram, self.mapping).map()

        ParentCalculatorTransformer(self.diagram).transform()
        DefaultTrustZoneTransformer(self.diagram).transform()

        return self.__build_otm()

    def __build_otm(self):
        otm = OTMBuilder(self.project_id, self.project_name, DiagramType.DRAWIO).build()

        otm.representations = [self.diagram.representation.otm]
        otm.components = [c.otm for c in self.diagram.components]
        otm.dataflows = [d.otm for d in self.diagram.dataflows]
        otm.trustzones = [t.otm for t in self.diagram.trustzones]

        return otm

