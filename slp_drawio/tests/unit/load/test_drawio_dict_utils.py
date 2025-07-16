# class TestDrawioDictUtils:
import json
from unittest.mock import patch

import pytest

from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load import drawio_dict_utils
from slp_drawio.tests.resources import test_resource_paths


def test_get_attributes_mx_cell_without_style_attr():
    # GIVEN an empty mx_cell
    mx_cell = {}

    # WHEN drawio_dict_utils::get_attributes
    attributes = drawio_dict_utils.get_attributes(mx_cell)

    # THEN attributes is empty
    assert len(attributes) == 0


def test_get_attributes():
    # GIVEN a mx_cell with style attr
    mx_cell = {
        "style": "outlineConnect=0;dashed=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;image=as="
    }

    # WHEN drawio_dict_utils::get_attributes
    attributes = drawio_dict_utils.get_attributes(mx_cell)

    # THEN attributes has the following data
    assert len(attributes) == 5
    assert attributes.get('outlineConnect') == "0"
    assert attributes.get('dashed') == "0"
    assert attributes.get('shape') == "mxgraph.aws4.group"
    assert attributes.get('grIcon') == "mxgraph.aws4.group_aws_cloud_alt"
    assert attributes.get('image') == "as="


@pytest.mark.parametrize('source, expected', [
    pytest.param({"mxfile": {"diagram": ['a', 'b']}}, True, id="is multiple page"),
    pytest.param({"mxfile": {"diagram": 'a'}}, False, id="is single page"),
])
def test_is_multiple_pages(source, expected):
    assert drawio_dict_utils.is_multiple_pages(source) == expected


@pytest.mark.parametrize('source,expected', [
    pytest.param({'mxfile': {'diagram': {'mxGraphModel': {'pageHeight': 123, 'pageWidth': 456}}}},
                 {'height': 123, 'width': 456},
                 id='exists size'),
    pytest.param({'mxGraphModel': {'pageHeight': 123, 'pageWidth': 456}},
                 {'height': 123, 'width': 456},
                 id='exists size only mxGraphModel'),
    pytest.param({'mxfile': {'diagram': {'mxGraphModel': {}}}}, None, id='not dimensions'),
    pytest.param({'mxGraphModel': {}}, None, id='not dimensions only mxGraphModel'),
    pytest.param({}, None, id='not model')
])
def test_get_diagram_size(source, expected):
    # GIVEN a mxfile diagram
    # WHEN drawio_dict_utils::test_get_diagram_size is called
    size = drawio_dict_utils.get_diagram_size(source)

    # THEN the size of the diagram or the default is returned
    assert size == expected


def test_get_mx_cell_components():
    # GIVEN a DrawIO with one component and Dataflow with multiple configurations
    source = json.loads(get_byte_data(test_resource_paths.aws_two_component_multiple_dataflows_as_json))

    # WHEN drawio_dict_utils::get_components_from_source
    components = drawio_dict_utils.get_mx_cell_components(source)

    # THEN it returns a unique component
    assert len(components) == 2


def test_get_mx_cell_dataflows():
    # GIVEN a DrawIO with one component and Dataflow with multiple configurations
    source = json.loads(get_byte_data(test_resource_paths.aws_two_component_multiple_dataflows_as_json))

    # WHEN drawio_dict_utils::get_components_from_source
    dataflows = drawio_dict_utils.get_mx_cell_dataflows(source)

    # THEN it returns 5 dataflows
    assert len(dataflows) == 5


@patch('slp_drawio.slp_drawio.load.drawio_dict_utils.__get_mx_cells')
@pytest.mark.parametrize('dataflow_id, source, expected', [
    pytest.param('1', [], [], id="tags are empty"),
    pytest.param('1', [{'parent': '2'}, {'parent': '1', 'value': 'tag'}], ['tag'], id="tags has one value"),
    pytest.param('1', [{'parent': '1', 'value': 'tag'}, {'parent': '1', 'value': 'tag2'}], ['tag', 'tag2'],
                 id="tags has two values"),
    pytest.param('1', [{'parent': '2', 'value': 'tag'}], [], id="tags is empty as not child exists"),
    pytest.param('1', [{'parent': '1'}], [], id="tags is empty as not value exists"),
])
def test_get_dataflow_tags(__get_mx_cells_mock, dataflow_id: str, source, expected):
    # GIVEN the dataflow_id
    # AND the get_mx_cells returning the given source
    __get_mx_cells_mock.return_value = source

    # WHEN drawio_dict_utils::get_dataflow_tags
    tags = drawio_dict_utils.get_dataflow_tags(dataflow_id, {})

    # THEN the tags are as expected
    assert tags == expected


@pytest.mark.parametrize('mx_geometry, expected', [
    pytest.param({}, {'x': 0, 'y': 0}, id="without position"),
    pytest.param({'x': '10'}, {'x': 10, 'y': 0}, id="only with x value"),
    pytest.param({'y': '10'}, {'x': 0, 'y': 10}, id="only with y value"),
    pytest.param({'x': '10.1', 'y': '20.9'}, {'x': 10, 'y': 21}, id="with x, y value"),
])
def test_get_position(mx_geometry, expected):
    # GIVEN a mx_cell with the given mxGeometry
    mx_cell = {"mxGeometry": mx_geometry}

    # WHEN drawio_dict_utils::get_component_position
    position = drawio_dict_utils.get_position(mx_cell)

    # THEN position has the following data
    assert position == expected


@pytest.mark.parametrize('mx_geometry, expected', [
    pytest.param({'height': '10.1', 'width': '20.9'}, {'height': 10, 'width': 21}, id="with height, width value"),
])
def test_get_size(mx_geometry, expected):
    # GIVEN a mx_cell with the given mxGeometry
    mx_cell = {"mxGeometry": mx_geometry}

    # WHEN drawio_dict_utils::get_component_size
    size = drawio_dict_utils.get_size(mx_cell)

    # THEN attributes has the following data
    assert size == expected
