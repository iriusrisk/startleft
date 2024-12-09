import json
from unittest.mock import patch

from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load.diagram_dataflow_loader import DiagramDataflowLoader
from slp_drawio.slp_drawio.load.drawio_dict_utils import get_dataflow_tags
from slp_drawio.tests.resources import test_resource_paths


class TestDiagramDataflowLoader:

    @patch('slp_drawio.slp_drawio.load.diagram_dataflow_loader.get_dataflow_tags', wraps=get_dataflow_tags)
    def test_load(self, get_dataflow_tags_wrapper):
        # GIVEN a DrawIO
        source = json.loads(get_byte_data(test_resource_paths.aws_two_component_multiple_dataflows_as_json))

        # WHEN DiagramDataflowLoader::load
        diagram_dataflows = DiagramDataflowLoader(source).load()

        # THEN diagram dataflows has length of 2
        assert len(diagram_dataflows) == 2
        # AND elements has the following information
        assert diagram_dataflows[0].otm.id == 'pt2kyrPXSm7H56EBWWGj-6'
        assert diagram_dataflows[0].otm.name == 'pt2kyrPXSm7H56EBWWGj-6-dataflow'
        assert diagram_dataflows[0].otm.source_node == 'pt2kyrPXSm7H56EBWWGj-1'
        assert diagram_dataflows[0].otm.destination_node == 'pt2kyrPXSm7H56EBWWGj-7'
        assert len(diagram_dataflows[0].otm.tags) == 1
        assert diagram_dataflows[0].otm.tags[0] == 'Dataflow Info'

        # AND self reference dataflow is also mapped
        assert diagram_dataflows[1].otm.id == 'pt2kyrPXSm7H56EBWWGj-8'
        assert diagram_dataflows[1].otm.name == 'pt2kyrPXSm7H56EBWWGj-8-dataflow'
        assert diagram_dataflows[1].otm.source_node == 'pt2kyrPXSm7H56EBWWGj-7'
        assert diagram_dataflows[1].otm.destination_node == 'pt2kyrPXSm7H56EBWWGj-7'
        assert not diagram_dataflows[1].otm.tags

        # AND the method get_dataflow_tags has been called once for each dataflow
        assert get_dataflow_tags_wrapper.call_count == len(diagram_dataflows)
