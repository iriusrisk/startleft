from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from otm.otm.otm_builder import OTMBuilder

from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import DiagramType
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram
from slp_drawio.slp_drawio.parse.diagram_mapper import DiagramMapper


class DrawioParser(ProviderParser):
    """
    Parser to build an OTM from DrawIO
    """

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping: DrawioMapping):
        self.diagram = diagram
        self.mapping = mapping
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

    def build_otm(self) -> OTM:
        self.map_components_and_trustzones()

        # TODO Implement and call Transformers here

        otm = self.__build_otm()

        return otm

    def map_components_and_trustzones(self):
        DiagramMapper(self.diagram, self.mapping).map()

    def __build_otm(self):
        otm = OTMBuilder(self.project_id, self.project_name, DiagramType.DRAWIO).build()

        otm.components = [c.otm for c in self.diagram.components]
        otm.dataflows = [d.otm for d in self.diagram.dataflows]
        otm.trustzones = [t.otm for t in self.diagram.trustzones]

        return otm

