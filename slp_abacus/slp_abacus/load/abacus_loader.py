import json
import logging
import yaml

from sl_util.sl_util.file_utils import read_byte_data
from slp_abacus.slp_abacus.objects.diagram_objects import Diagram, DiagramComponent, DiagramRepresentation
from slp_base import LoadingDiagramFileError
from slp_base.slp_base.provider_loader import ProviderLoader

logger = logging.getLogger(__name__)


class AbacusLoader(ProviderLoader):
    """
    Builder for an Abacus class from the json data
    """

    def __init__(self, project_id: str, abacus_source, mapping_files: [bytes]):
        self.project_id = project_id
        self.abacus_source = abacus_source
        self.mapping_files = mapping_files

        self._diagram = None

    def load(self):
        try:
            # Parse JSON and YAML data
            out_connections = json.loads(read_byte_data(self.abacus_source))["OutConnections"]

            abacus_mapping: str = read_byte_data(self.mapping_files[0])
            component_mappings = yaml.safe_load(abacus_mapping)['components']

            # Perform the mapping

            representation: DiagramRepresentation = DiagramRepresentation(self.project_id,
                                                                          {'width': 1000, 'height': 1000})
            diagram_components = self.map_to_diagram_components(out_connections, component_mappings)

            # Output the list of DiagramComponent objects
            for component in diagram_components:
                print(component)

            self._diagram: Diagram = Diagram(representation, diagram_components, {})
            return diagram_components

        except LoadingDiagramFileError as e:
            raise e
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingDiagramFileError('Source file cannot be loaded', detail, message)

    # Function to map JSON data to DiagramComponent objects
    def map_to_diagram_components(self, out_connections: [dict], component_mappings: [dict]):
        diagram_components = []

        for connection in out_connections:
            # for mapping in component_mappings:
            id_str: str = str(connection["EEID"])
            if not any(c.otm.id == id_str for c in diagram_components):
                diagram_components.append(
                    DiagramComponent(id=str(connection["EEID"]), name=connection["SinkComponentName"],
                                     shape_type=connection["ConnectionTypeName"]))

        return diagram_components

    def get_diagram(self) -> Diagram:
        return self._diagram
