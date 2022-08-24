from otm.otm.otm import Component, Dataflow, Trustzone
from otm.otm.otm_builder import OtmBuilder
from startleft.startleft.diagram.mapping.diagram_pruner import DiagramPruner
from startleft.startleft.diagram.mapping.mappers.diagram_component_mapper import DiagramComponentMapper
from startleft.startleft.diagram.mapping.mappers.diagram_connector_mapper import DiagramConnectorMapper
from startleft.startleft.diagram.mapping.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper
from startleft.startleft.diagram.mapping.visio_mapping_loader import DiagramMappingLoader
from startleft.startleft.diagram.objects.diagram_objects import Diagram


class DiagramToOtm:

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_file):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = DiagramMappingLoader(mapping_file)

        self.__trustzone_mappings = None
        self.__component_mappings = None
        self.__default_trustzone = None

    def run(self):
        self.__load_mappings()
        self.__prune_diagram()

        return self.__build_otm(self.__map_trustzones(), self.__map_components(), self.__map_dataflows())

    def __load_mappings(self):
        self.__trustzone_mappings, self.__component_mappings = self.mapping_loader.load_mappings()

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
        return OtmBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_default_trustzone(self.__default_trustzone) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(dataflows) \
            .build()
