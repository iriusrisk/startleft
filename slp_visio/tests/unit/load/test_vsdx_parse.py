from slp_base import DiagramType

from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponentOrigin

from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioComponentFactory, VisioConnectorFactory

from slp_visio.slp_visio.load.vsdx_parser import VsdxParser
from slp_visio.tests.resources import test_resource_paths

class TestVsdxParser:

    def test_name_in_child_shape(self):
        # GIVEN the parser
        parser = VsdxParser(VisioComponentFactory(), VisioConnectorFactory())
        # WHEN we parse the vsdx file
        diagram : Diagram = parser.parse(test_resource_paths.visio_complex_stencil_text)
        # THEN we check the components created
        assert diagram.diagram_type == DiagramType.VISIO
        assert len( diagram.connectors) == 0
        assert len( diagram.components) == 1
        assert diagram.components[0].name == 'Custom AWS Step Functions workflow name'
        assert diagram.components[0].origin == DiagramComponentOrigin.SIMPLE_COMPONENT
