from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.parse.mtmt_connector_parser import MTMTConnectorParser
from slp_mtmt.tests.resources import test_resource_paths


class TestMTMTConnectorParser:

    def test_parse_connectors(self):
        # GIVEN the source Mtmt data
        with open(test_resource_paths.model_mtmt_mvp, 'r') as f:
            xml = f.read()
        # AND the provider loader
        mtmt: MTMTLoader = MTMTLoader(xml)
        mtmt.load()

        # AND the parser
        parser = MTMTConnectorParser(mtmt.get_mtmt())

        # WHEN the parse method is called
        dataflows = parser.parse()

        # THEN the response is the expected
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
