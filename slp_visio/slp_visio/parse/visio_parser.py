from slp_visio.slp_visio.load.objects.diagram_objects import Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper
from otm.otm.otm import Component, Dataflow, Trustzone
from otm.otm.otm_builder import OtmBuilder
from slp_base import ProviderParser


class VisioParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = mapping_loader

        self.__trustzone_mappings = self.mapping_loader.get_trustzone_mappings()
        self.__component_mappings = self.mapping_loader.get_component_mappings()
        self.__default_trustzone = None

    def build_otm(self):
        self.__prune_diagram()

        return self.__build_otm(self.__map_trustzones(), self.__map_components(), self.__map_dataflows())

    def __prune_diagram(self):
        DiagramPruner(self.diagram, self.mapping_loader.get_all_labels()).run()

    def __map_trustzones(self):
        trustzone_mapper = DiagramTrustzoneMapper(self.diagram.components, self.__trustzone_mappings)
        self.__default_trustzone = trustzone_mapper.get_default_trustzone()
        return trustzone_mapper.to_otm()

    def __map_components(self):
        return DiagramComponentMapper(
            self.diagram.components,
            self.__component_mappings,
            self.__trustzone_mappings,
            self.__default_trustzone).to_otm()

    def __map_dataflows(self):
        return DiagramConnectorMapper(self.diagram.connectors).to_otm()

    def __build_otm(self, trustzones: [Trustzone], components: [Component], dataflows: [Dataflow]):
        otm_builder = OtmBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(dataflows)

        if self.__default_trustzone:
            otm_builder.add_default_trustzone(self.__default_trustzone)

        return otm_builder.build()
