from startleft.api.errors import UnknownDiagramType
from startleft.diagram.diagram_type import DiagramType
from startleft.diagram.mapping.diagram_to_otm import DiagramToOtm
from startleft.diagram.objects.visio.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory
from startleft.diagram.parsers.visio.visio_diagram_parser import VisioDiagramParser
from startleft.otm.otm import OTM


def get_parser_for_diagram_type(provider):
    if provider == DiagramType.VISIO:
        return VisioDiagramParser(VisioComponentFactory(), VisioConnectorFactory())

    raise UnknownDiagramType


class ExternalDiagramToOtm:
    def __init__(self, diagram_type: DiagramType):
        self.diagram_type = diagram_type

    def run(self, diagram_source: str, mapping_file, project_name: str, project_id: str) -> OTM:
        diagram = get_parser_for_diagram_type(self.diagram_type).parse(diagram_source)

        return DiagramToOtm(
            project_id=project_id,
            project_name=project_name,
            diagram=diagram,
            mapping_file=mapping_file
        ).run()
