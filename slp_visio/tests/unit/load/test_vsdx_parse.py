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
        assert diagram.components[0].origin == DiagramComponentOrigin.SIMPLE_COMPONENT
        assert diagram.components[0].name == 'AWS Step Functions workflow'
        assert diagram.components[0].id == '1'


    def test_shape_group(self):
        # GIVEN the parser
        parser = VsdxParser(VisioComponentFactory(), VisioConnectorFactory())
        # WHEN we parse the vsdx file
        diagram : Diagram = parser.parse(test_resource_paths.visio_shape_group)
        # THEN we check the components created
        assert diagram.diagram_type == DiagramType.VISIO
        assert len( diagram.connectors) == 0
        assert len( diagram.components) == 3
        for component in diagram.components:
            assert component.origin == DiagramComponentOrigin.SIMPLE_COMPONENT
        assert diagram.components[0].name == 'My Cloud Menu'
        assert diagram.components[0].id == '1'
        assert diagram.components[1].name == 'My AAD Cloud Sync Menu'
        assert diagram.components[1].id == '3'
        assert diagram.components[2].name == 'My Keys Menu'
        assert diagram.components[2].id == '9'

    def test_children_with_same_relative_coordinates(self):
        # GIVEN the parser
        parser = VsdxParser(VisioComponentFactory(), VisioConnectorFactory())
        # WHEN we parse the vsdx file
        diagram : Diagram = parser.parse(test_resource_paths.lucid_two_children_same_relative_coordinates)
        # THEN we check the components created
        assert diagram.diagram_type == DiagramType.VISIO
        assert len( diagram.connectors) == 0
        assert len( diagram.components) == 6
        for component in diagram.components:
            assert component.origin == DiagramComponentOrigin.SIMPLE_COMPONENT
        assert diagram.components[0].name == 'VPC1'
        assert diagram.components[0].id == '2'
        assert diagram.components[1].name == 'Application Load Balancer TLS 1.2 A1'
        assert diagram.components[1].id == '7'
        assert diagram.components[2].name == 'GIT/Kubernetes ECS1'
        assert diagram.components[2].id == '10'
        assert diagram.components[3].name == 'VPC2'
        assert diagram.components[3].id == '15'
        assert diagram.components[4].name == 'Application Load Balancer TLS 1.2 A2'
        assert diagram.components[4].id == '20'
        assert diagram.components[5].name == 'GIT/Kubernetes ECS2'
        assert diagram.components[5].id == '23'

