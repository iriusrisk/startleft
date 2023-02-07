from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from otm.otm.otm_builder import OtmBuilder
from otm.otm.otm_pruner import OtmPruner
from slp_base import ProviderParser
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator, \
    build_size_object, calculate_diagram_size


class VisioParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = mapping_loader

        self.representation_id = f'{self.project_id}-diagram'
        self.representations = [
            DiagramRepresentation(
                id_=self.representation_id,
                name=f'{self.project_id} Diagram Representation',
                type_=str(RepresentationType.DIAGRAM.value),
                size=build_size_object(calculate_diagram_size(self.diagram.limits))
            )
        ]

        self._representation_calculator = RepresentationCalculator(self.representation_id, self.diagram.limits)
        self._trustzone_mappings = self.mapping_loader.get_trustzone_mappings()
        self._component_mappings = self.mapping_loader.get_component_mappings()
        self._default_trustzone = None

    def build_otm(self):
        self.__prune_diagram()

        otm_builder = OtmBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_representations(self.representations, extend=False) \
            .add_trustzones(self._map_trustzones()) \
            .add_components(self._map_components()) \
            .add_dataflows(self._map_dataflows())

        if self._default_trustzone:
            otm_builder.add_default_trustzone(self._default_trustzone)

        otm = otm_builder.build()

        OtmPruner(otm).prune_orphan_dataflows()

        return otm

    def __prune_diagram(self):
        DiagramPruner(self.diagram, self.mapping_loader.get_all_labels()).run()

    def _map_trustzones(self):
        trustzone_mapper = DiagramTrustzoneMapper(
            self.diagram.components,
            self._trustzone_mappings,
            self._representation_calculator
        )

        self._default_trustzone = trustzone_mapper.get_default_trustzone()
        return trustzone_mapper.to_otm()

    def _map_components(self):
        return DiagramComponentMapper(
            self.diagram.components,
            self._component_mappings,
            self._trustzone_mappings,
            self._default_trustzone,
            self._representation_calculator,
        ).to_otm()

    def _map_dataflows(self):
        return DiagramConnectorMapper(self.diagram.connectors).to_otm()
