from otm.otm.entity.component import OtmComponent
from otm.otm.entity.dataflow import OtmDataflow
from otm.otm.entity.trustzone import OtmTrustzone
from otm.otm.otm_builder import OtmBuilder
from slp_base import ProviderParser
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper


def prune_orphan_dataflows(dataflows: [OtmDataflow], components: [OtmComponent]):
    valids = []
    for dataflow in dataflows:
        source = False
        destination = False
        for component in components:
            if dataflow.source_node == component.id:
                source = True
                continue
            if dataflow.destination_node == component.id:
                destination = True
                continue
        if destination and source:
            valids.append(dataflow)
            continue
    return valids


class VisioParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = mapping_loader

        self._trustzone_mappings = self.mapping_loader.get_trustzone_mappings()
        self._component_mappings = self.mapping_loader.get_component_mappings()
        self._default_trustzone = None

    def build_otm(self):
        self.__prune_diagram()

        return self._build_otm(self._map_trustzones(), self._map_components(), self._map_dataflows())

    def __prune_diagram(self):
        DiagramPruner(self.diagram, self.mapping_loader.get_all_labels()).run()

    def _map_trustzones(self):
        trustzone_mapper = DiagramTrustzoneMapper(self.diagram.components, self._trustzone_mappings)
        self._default_trustzone = trustzone_mapper.get_default_trustzone()
        return trustzone_mapper.to_otm()

    def _map_components(self):
        return DiagramComponentMapper(
            self.diagram.components,
            self._component_mappings,
            self._trustzone_mappings,
            self._default_trustzone).to_otm()

    def _map_dataflows(self):
        return DiagramConnectorMapper(self.diagram.connectors).to_otm()

    def _build_otm(self, trustzones: [OtmTrustzone], components: [OtmComponent], dataflows: [OtmDataflow]):
        connected_dataflows = prune_orphan_dataflows(dataflows, components)
        otm_builder = OtmBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(connected_dataflows)

        if self._default_trustzone:
            otm_builder.add_default_trustzone(self._default_trustzone)

        return otm_builder.build()
