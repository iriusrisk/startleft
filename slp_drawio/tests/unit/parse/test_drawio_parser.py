from unittest.mock import Mock, patch

from pytest import raises

from slp_base import OTMBuildingError
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramTrustZone, DiagramRepresentation, \
    DiagramDataflow
from slp_drawio.slp_drawio.parse.drawio_parser import DrawioParser
from slp_drawio.tests.util.builders import build_component


class TestDrawioParser:

    @patch('slp_drawio.slp_drawio.parse.drawio_parser.DiagramMapper')
    @patch('slp_drawio.slp_drawio.parse.drawio_parser.ParentCalculatorTransformer')
    @patch('slp_drawio.slp_drawio.parse.drawio_parser.DefaultTrustZoneTransformer')
    def test_parsed_ok(self, mapper_mock, parent_calculator_mock, default_tz_transformer_mock):
        # GIVEN a diagram with some trustzones, components and dataflows
        representation = DiagramRepresentation(project_id='1', size={})
        trustzones = [DiagramTrustZone(type_='1'), DiagramTrustZone(type_='1')]
        components = [build_component(component_id='1'), build_component(component_id='1')]
        dataflows = [DiagramDataflow(dataflow_id='1'), DiagramDataflow(dataflow_id='2')]
        diagram = Diagram(
            representation=representation,
            trustzones=trustzones,
            components=components,
            dataflows=dataflows)

        # WHEN DrawioParser::build_otm is called
        otm = DrawioParser(project_id='id', project_name='name', diagram=diagram, mapping=Mock()).build_otm()

        # THEN the components are mapped
        mapper_mock.assert_called_once()

        # AND all the transformers are executed once
        parent_calculator_mock.assert_called_once()
        default_tz_transformer_mock.assert_called_once()

        # AND an OTM is returned with all the elements present
        assert otm.project_id == 'id'
        assert otm.project_name == 'name'
        assert otm.representations == [diagram.representation.otm]
        assert otm.components == [c.otm for c in diagram.components]
        assert otm.dataflows == [d.otm for d in diagram.dataflows]
        assert otm.trustzones == [t.otm for t in diagram.trustzones]

    @patch('slp_drawio.slp_drawio.parse.drawio_parser.DiagramMapper.map')
    def test_controlled_exception(self, map_mock):
        # GIVEN a parser with mocked arguments
        # AND a forced OTMBuildingError exception
        title= 'Error title'
        detail = 'Error detail'
        map_mock.side_effect = OTMBuildingError(title, detail)

        # WHEN DrawioParser::build_otm is called
        with raises(OTMBuildingError) as error:
            DrawioParser(project_id='id', project_name='name', diagram=Mock(), mapping=Mock()).build_otm()

        # THEN the exception is re-raised
        assert error.value.title == title
        assert error.value.detail == detail

    @patch('slp_drawio.slp_drawio.parse.drawio_parser.DiagramMapper.map')
    def test_uncontrolled_exception(self, map_mock):
        # GIVEN a parser with mocked arguments
        # AND a forced uncontrolled exception
        message= 'Error message'
        map_mock.side_effect = Exception(message)

        # WHEN DrawioParser::build_otm is called
        with raises(OTMBuildingError) as error:
            DrawioParser(project_id='id', project_name='name', diagram=Mock(), mapping=Mock()).build_otm()

        # THEN the exception is encapsulated in an OTMBuildingError
        assert error.value.title == 'Error building the threat model with the given files'
        assert error.value.message == 'Error message'
        assert error.value.detail == 'Exception'
