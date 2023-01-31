from otm.otm.entity.dataflow import OtmDataflow
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.tests.unit.util.test_uuid import is_valid_uuid


class TestDiagramConnectorMapper:

    def test_to_otm(self):
        # GIVEN a list of DiagramConnector
        connectors = [DiagramConnector('k1', 'c100', 'c200', name='Diagram connector 1'),
                      DiagramConnector('k2', 'c200', 'c100', name='Diagram connector 2', bidirectional=True),
                      DiagramConnector('k3', 'c300', 'c400', bidirectional=False),
                      DiagramConnector('k4', '', ''),
                      DiagramConnector('k5', None, None), DiagramConnector(None, None, None)]

        # AND the mapper
        mapper = DiagramConnectorMapper(connectors)

        # WHEN calling to_otm
        otm: [OtmDataflow] = mapper.to_otm()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm) == 6
        assert otm[0].id == 'k1'
        assert otm[0].source_node == 'c100'
        assert otm[0].destination_node == 'c200'
        assert otm[0].name == 'Diagram connector 1'
        assert not otm[0].bidirectional
        assert otm[1].id == 'k2'
        assert otm[1].source_node == 'c200'
        assert otm[1].destination_node == 'c100'
        assert otm[1].name == 'Diagram connector 2'
        assert otm[1].bidirectional
        assert otm[2].id == 'k3'
        assert otm[2].source_node == 'c300'
        assert otm[2].destination_node == 'c400'
        assert is_valid_uuid(otm[2].name)
        assert not otm[2].bidirectional
        assert otm[3].id == 'k4'
        assert otm[3].source_node == ''
        assert otm[3].destination_node == ''
        assert is_valid_uuid(otm[3].name)
        assert not otm[3].bidirectional
        assert otm[4].id == 'k5'
        assert otm[4].source_node is None
        assert otm[4].destination_node is None
        assert is_valid_uuid(otm[4].name)
        assert not otm[4].bidirectional
        assert otm[5].id is None
        assert otm[5].source_node is None
        assert otm[5].destination_node is None
        assert is_valid_uuid(otm[5].name)
        assert not otm[5].bidirectional
