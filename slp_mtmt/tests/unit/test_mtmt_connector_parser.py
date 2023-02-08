from pytest import mark

from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from sl_util.sl_util.file_utils import get_byte_data
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.parse.mtmt_connector_parser import MTMTConnectorParser
from slp_mtmt.tests.resources import test_resource_paths

SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mtmt_default_mapping


class TestMTMTConnectorParser:

    def test_parse_connectors(self):
        # GIVEN a valid MTMT file
        xml = get_byte_data(SAMPLE_VALID_MTMT_FILE)
        mtmt_loader: MTMTLoader = MTMTLoader(xml)
        mtmt_loader.load()
        mtmt = mtmt_loader.get_mtmt()

        # AND the connector parser
        parser = MTMTConnectorParser(mtmt)

        # WHEN the parse method is called
        dataflows = parser.parse()

        # THEN the response is the expected
        assert len(dataflows) == 6
        dataflow = dataflows[0]
        assert dataflow.id == 'eb072144-af37-4b75-b46b-b78111850d3e'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert not dataflow.bidirectional
        dataflow = dataflows[1]
        assert dataflow.id == '36091fd8-dba8-424e-a3cd-784ea6bcb9e0'
        assert dataflow.source_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = dataflows[2]
        assert dataflow.id == 'f5fe3c6e-e10b-4252-a4aa-4ec6108c96a6'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '91882aca-8249-49a7-96f0-164b68411b48'
        dataflow = dataflows[3]
        assert dataflow.id == 'd826de3d-1464-4d1f-8105-aa0449a50aec'
        assert dataflow.source_node == '91882aca-8249-49a7-96f0-164b68411b48'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = dataflows[4]
        assert dataflow.id == '9840bcdf-c444-437d-8289-d5468f41b0db'
        assert dataflow.source_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = dataflows[5]
        assert dataflow.id == '5861370d-b333-4d4b-9420-95425026e9c9'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'

    @mark.parametrize('source,target,expected', [
        ('ad9a677a-6a4a-11ed-b01f-6bc89d9a4150', 'b6596e2e-6a4a-11ed-b8d3-237d9695ac03', 1),
        ('00000000-0000-0000-0000-000000000001', 'b6596e2e-6a4a-11ed-b8d3-237d9695ac03', 1),
        ('b6596e2e-6a4a-11ed-b8d3-237d9695ac03', '00000000-0000-0000-0000-000000000001', 1),
        ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 1),
        ('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 0),
        ('00000000-0000-0000-0000-000000000000', 'b6596e2e-6a4a-11ed-b8d3-237d9695ac03', 0),
        ('ad9a677a-6a4a-11ed-b01f-6bc89d9a4150', '00000000-0000-0000-0000-000000000000', 0),
        ('', '', 0),
        ('', 'b6596e2e-6a4a-11ed-b8d3-237d9695ac03', 0),
        ('b6596e2e-6a4a-11ed-b8d3-237d9695ac03', '', 0),
        ('abc', '', 0),
        ('b6596e2e-6a4a-11ed-b8d3-237d9695ac0', '', 0),
    ])
    def test_parse_orphan_connectors(self, source, target, expected):
        # Given the line
        line_source = {'Key': 'eb072144-af37-4b75-b46b-b78111850d3e', 'Value': {
            'Properties': {
                'anyType': [{'DisplayName': 'Request', 'Value': {}},
                            {'DisplayName': 'Name', 'Value': {'text': 'PSQL Request'}},
                            ], },
            'HandleX': '892', 'HandleY': '210',
            'SourceGuid': f'{source}',
            'SourceX': '846', 'SourceY': '261',
            'TargetGuid': f'{target}',
            'TargetX': '980', 'TargetY': '232'},
                       'attrib': {'type': 'Connector'}}
        line = MTMLine(line_source)

        # And the mtmt source with the line
        mtmt = MTMT(None, [line], None, None)

        # And the parser
        parser = MTMTConnectorParser(mtmt)

        # When we call the parser
        dataflows = parser.parse()

        # Then we check the otm dataflows created
        assert len(dataflows) == expected
