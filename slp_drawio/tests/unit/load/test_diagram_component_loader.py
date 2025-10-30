import json
from unittest.mock import patch

from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load.diagram_component_loader import DiagramComponentLoader
from slp_drawio.slp_drawio.load.drawio_dict_utils import get_size, get_position
from slp_drawio.tests.resources import test_resource_paths


class TestDiagramComponentLoader:
    PROJECT_ID = 'drawio-project'

    def test_aws_minimal_drawio(self):
        # GIVEN a DrawIO
        source = json.loads(get_byte_data(test_resource_paths.aws_minimal_drawio_as_json))

        # WHEN DiagramComponentLoader::load
        diagram_components = DiagramComponentLoader(self.PROJECT_ID, source).load()

        # THEN diagram components has length of 4
        assert len(diagram_components) == 4
        # AND elements have the following information
        assert diagram_components[0].otm.id == "5i7VU8sxTlh_DojUgWXD-1"
        assert diagram_components[0].otm.name == "AWS Cloud"
        assert diagram_components[0].shape_type == "aws.group_aws_cloud_alt"
        assert not diagram_components[0].shape_parent_id
        assert len(diagram_components[0].otm.representations) == 1
        assert list(diagram_components[0].otm.representations[0].attributes.keys()) == ['style']

        assert diagram_components[1].otm.id == "xUHJV5QXkyTOu5aMK-rF-2"
        assert not diagram_components[1].otm.name
        assert not diagram_components[1].shape_type
        assert diagram_components[1].shape_parent_id == "5i7VU8sxTlh_DojUgWXD-1"

        assert diagram_components[2].otm.id == "5i7VU8sxTlh_DojUgWXD-2"
        assert diagram_components[2].otm.name == "Region"
        assert diagram_components[2].shape_type == "aws.group_region"
        assert not diagram_components[2].shape_parent_id

        assert diagram_components[3].otm.id == "xUHJV5QXkyTOu5aMK-rF-3"
        assert not diagram_components[3].otm.name
        assert diagram_components[3].shape_type == "aws.ec2"
        assert diagram_components[3].shape_parent_id == "5i7VU8sxTlh_DojUgWXD-2"

    @patch('slp_drawio.slp_drawio.load.diagram_component_loader.get_size', wraps=get_size)
    @patch('slp_drawio.slp_drawio.load.diagram_component_loader.get_position', wraps=get_position)
    def test_get_representation_element(self, get_size_wrapper, get_position_wrapper):
        # GIVEN the mx_cell with the following attributes
        mx_cell = {
            'id': 'mx-cell-identifier',
            'style': "spacingLeft=30;fontColor=#232F3E;dashed=0;",
            'mxGeometry': {'x': '100', 'y': '200', 'height': '10', 'width': '20'}
        }

        # WHEN DiagramComponentLoader::__get_representation_element
        representation_element = DiagramComponentLoader(self.PROJECT_ID, {})._get_representation_element(mx_cell)

        # THEN the representation is as expected
        get_size_wrapper.assert_called_once()
        get_position_wrapper.assert_called_once()

        assert representation_element.id == "mx-cell-identifier-diagram"
        assert representation_element.name == "mx-cell-identifier Representation"
        assert representation_element.representation == f"{self.PROJECT_ID}-diagram"
        assert representation_element.position == {'x': 100, 'y': 200}
        assert representation_element.size == {'height': 10, 'width': 20}
        assert representation_element.attributes['style'] == "spacingLeft=30;fontColor=#232F3E;dashed=0;"
