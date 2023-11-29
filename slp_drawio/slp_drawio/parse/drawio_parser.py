import logging

from otm.otm.entity.otm import OTM
from otm.otm.otm_builder import OTMBuilder
from slp_base import OTMBuildingError
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import DiagramType
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram
from slp_drawio.slp_drawio.parse.diagram_mapper import DiagramMapper
from slp_drawio.slp_drawio.parse.transformers.default_trustzone_transformer import DefaultTrustZoneTransformer
from slp_drawio.slp_drawio.parse.transformers.parent_calculator_transformer import ParentCalculatorTransformer

logger = logging.getLogger(__name__)


class DrawioParser(ProviderParser):
    """
    Parser to build an OTM from DrawIO
    """

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping: DrawioMapping):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping = mapping

    def build_otm(self) -> OTM:
        try:
            DiagramMapper(self.diagram, self.mapping).map()

            ParentCalculatorTransformer(self.diagram).transform()
            DefaultTrustZoneTransformer(self.diagram).transform()

            return self.__build_otm()
        except OTMBuildingError as e:
            raise e
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OTMBuildingError('Error building the threat model with the given files', detail, message)

    def __build_otm(self):
        otm = OTMBuilder(self.project_id, self.project_name, DiagramType.DRAWIO).build()

        otm.representations = [self.diagram.representation.otm]
        otm.components = [c.otm for c in self.diagram.components]
        otm.dataflows = [d.otm for d in self.diagram.dataflows]
        otm.trustzones = [t.otm for t in self.diagram.trustzones]

        return otm
