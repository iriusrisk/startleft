import json
from typing import Dict, List
from unittest.mock import patch

import pytest

from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load import diagram_component_loader
from slp_drawio.slp_drawio.load.diagram_component_loader import DiagramComponentLoader
from slp_drawio.slp_drawio.load.drawio_dict_utils import get_size, get_position
from slp_drawio.tests.resources import test_resource_paths


@pytest.mark.parametrize('source, result', [
    pytest.param(None, None, id="with Style None"),
    pytest.param('', None, id="with Style Empty"),
    pytest.param('shape=mxgraph.android.phone2;', 'android.phone2', id="from android"),
    pytest.param('shape=mxgraph.aws4.ec2', 'aws.ec2', id="from shape"),
    pytest.param('shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;',
                 'aws.group_aws_cloud_alt', id="from grIcon by group"),
    pytest.param('shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_elastic_load_balancing;',
                 'aws.group_elastic_load_balancing', id="from grIcon by groupCenter"),
    pytest.param('shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.queue;',
                 'aws.queue', id="from resIcon by resourceIcon"),
    pytest.param('shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.athena;',
                 'aws.athena', id="from prIcon by productIcon"),
])
def test_calculate_shape_type(source, result):
    # GIVEN a mxCell with the style
    mx_cell = {'style': source} if source else {}

    # WHEN diagram_component_loader::_calculate_shape_type
    shape_type = diagram_component_loader._calculate_shape_type(mx_cell)

    # THEN the shape_type is as expected
    assert shape_type == result


@pytest.mark.parametrize('mx_cell, components, expected', [
    pytest.param({}, [], None, id="with mxCell without parent None"),
    pytest.param({'parent': 1}, [{'id': 1}], 1, id="parent exists in components"),
    pytest.param({'parent': 1}, [{'id': 2}], None, id="parent not exists in components"),

])
def test_get_shape_parent_id(mx_cell: Dict, components: List, expected):
    # GIVEN a mx_cell
    # WHEN diagram_component_loader::_calculate_shape_type
    parent_id = diagram_component_loader._get_shape_parent_id(mx_cell, components)

    # THEN the parent is as expected
    assert parent_id == expected


@patch('slp_drawio.slp_drawio.load.diagram_component_loader._calculate_shape_type')
@pytest.mark.parametrize('mx_cell, shape_type, expected', [
    pytest.param({}, None, 'N/A', id="with mxCell without value and type"),
    pytest.param({'value': 'name'}, None, 'name', id="with mxCell with value"),
    pytest.param({'value': '1'}, None, '_1', id="with mxCell with len(value) is 1"),
    pytest.param({}, 'type', 'type', id="with mxCell without value, shape_type without dots"),
    pytest.param({}, 'type', 'type', id="with mxCell without value, shape_type with dot and underscore"),
    pytest.param({}, 'aws.type', 'type', id="with mxCell without value, shape_type with dot but without underscore"),
    pytest.param({}, 'mxgraph.aws.type', 'type',
                 id="with mxCell without value, shape_type with dots but without underscore"),
    pytest.param({}, 'component_type', 'component type', id="with mxCell without value, shape_type with underscore"),
    pytest.param({}, 'mxgraph.aws.component_type', 'component type',
                 id="with mxCell without value, shape_type with dots and underscore"),

])
def test_get_shape_name(_calculate_shape_type_mock, mx_cell: Dict, shape_type, expected):
    # GIVEN the mx_cell
    # AND a _calculate_shape_type that returns the given shape_type
    _calculate_shape_type_mock.return_value = shape_type
    # WHEN diagram_component_loader::_get_shape_name
    name = diagram_component_loader._get_shape_name(mx_cell)

    # THEN the parent is as expected
    assert name == expected


class TestDiagramComponentLoader:
    PROJECT_ID = 'drawio-project'

    def test_aws_minimal_drawio(self):
        # GIVEN a DrawIO
        source = json.loads(get_byte_data(test_resource_paths.aws_minimal_drawio_as_json))

        # WHEN DiagramComponentLoader::load
        diagram_components = DiagramComponentLoader(self.PROJECT_ID, source).load()

        # THEN diagram components has length of 4
        assert len(diagram_components) == 4
        # AND elements has the following information
        assert diagram_components[0].otm.id == "5i7VU8sxTlh_DojUgWXD-1"
        assert diagram_components[0].otm.name == "AWS Cloud"
        assert diagram_components[0].shape_type == "aws.group_aws_cloud_alt"
        assert diagram_components[0].shape_parent_id is None
        assert len(diagram_components[0].otm.representations) == 1
        assert list(diagram_components[0].otm.representations[0].attributes.keys()) == ['style']

        assert diagram_components[1].otm.id == "xUHJV5QXkyTOu5aMK-rF-2"
        assert diagram_components[1].otm.name == "N/A"
        assert diagram_components[1].shape_type is None
        assert diagram_components[1].shape_parent_id == "5i7VU8sxTlh_DojUgWXD-1"
        assert len(diagram_components[1].otm.representations) == 1
        assert list(diagram_components[1].otm.representations[0].attributes.keys()) == ['style']

        assert diagram_components[2].otm.id == "5i7VU8sxTlh_DojUgWXD-2"
        assert diagram_components[2].otm.name == "Region"
        assert diagram_components[2].shape_type == "aws.group_region"
        assert diagram_components[2].shape_parent_id is None
        assert len(diagram_components[2].otm.representations) == 1
        assert list(diagram_components[2].otm.representations[0].attributes.keys()) == ['style']

        assert diagram_components[3].otm.id == "xUHJV5QXkyTOu5aMK-rF-3"
        assert diagram_components[3].otm.name == "ec2"
        assert diagram_components[3].shape_type == "aws.ec2"
        assert diagram_components[3].shape_parent_id == "5i7VU8sxTlh_DojUgWXD-2"
        assert len(diagram_components[3].otm.representations) == 1
        assert list(diagram_components[3].otm.representations[0].attributes.keys()) == ['style']

    @patch('slp_drawio.slp_drawio.load.diagram_component_loader.get_size', wraps=get_size)
    @patch('slp_drawio.slp_drawio.load.diagram_component_loader.get_position', wraps=get_position)
    def test_get_representation_element(self, get_size_wrapper, get_position_wrapper):
        # GIVEN the mx_cell with the following attributes
        mx_cell = {
            'id': 'mx-cell-identifier',
            'style': "spacingLeft=30;fontColor=#232F3E;dashed=0",
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
        assert representation_element.attributes['style'] == "spacingLeft=30;fontColor=#232F3E;dashed=0"
