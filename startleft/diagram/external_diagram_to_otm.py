from startleft.api.errors import UnknownProvider
from startleft.diagram.converters.visio.visio_diagram_converter import VisioDiagramConverter
from startleft.diagram.diagram_to_otm import DiagramToOtm
from startleft.diagram.objects.visio.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from startleft.otm import OTM
from startleft.provider import Provider


def get_converter_for_provider(provider):
    if provider == Provider.VISIO:
        return VisioDiagramConverter(VisioComponentFactory(), VisioConnectorFactory())

    raise UnknownProvider


class ExternalDiagramToOtm:
    def __init__(self, diagram_type: Provider):
        self.diagram_type = diagram_type

    def run(self, diagram_source: str, mapping_file, project_name: str, project_id: str) -> OTM:
        diagram = get_converter_for_provider(self.diagram_type).convert_to_diagram(diagram_source)

        return DiagramToOtm(
            project_id=project_id,
            project_name=project_name,
            diagram=diagram,
            mapping_file=mapping_file
        ).run()
