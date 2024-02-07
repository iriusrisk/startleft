import logging

from otm.otm.entity.otm import OTM
from otm.otm.otm_builder import OTMBuilder
from slp_base import OTMBuildingError
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import DiagramType
from slp_abacus.slp_abacus.load.abacus_mapping_file_loader import AbacusMapping
from slp_abacus.slp_abacus.objects.diagram_objects import Diagram
from slp_abacus.slp_abacus.parse.diagram_mapper import DiagramMapper
from slp_abacus.slp_abacus.parse.transformers.default_trustzone_transformer import DefaultTrustZoneTransformer

logger = logging.getLogger(__name__)


class AbacusParser(ProviderParser):
    """
    Parser to build an OTM from Abacus
    """

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping: AbacusMapping):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping = mapping

    def build_otm(self) -> OTM:
        try:
            DiagramMapper(self.diagram, self.mapping).map()

            DefaultTrustZoneTransformer(self.diagram).transform()

            return self.__build_otm()
        except OTMBuildingError as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise e
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OTMBuildingError('Error building the threat model with the given files', detail, message)

    def __build_otm(self):
        otm = OTMBuilder(self.project_id, self.project_name, DiagramType.ABACUS).build()

        otm.representations = [self.diagram.representation.otm]
        otm.components = [c.otm for c in self.diagram.components]
        otm.dataflows = [d.otm for d in self.diagram.dataflows]
        otm.trustzones = [t.otm for t in self.diagram.trustzones]

        return otm
