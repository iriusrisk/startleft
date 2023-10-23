
# class TestDrawioDictUtils:
import json

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
        "style": "outlineConnect=0;dashed=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;"
    }

    # WHEN drawio_dict_utils::get_attributes
    attributes = drawio_dict_utils.get_attributes(mx_cell)

    # THEN attributes has the following data
    assert len(attributes) == 4
    assert attributes.get('outlineConnect') == "0"
    assert attributes.get('dashed') == "0"
    assert attributes.get('shape') == "mxgraph.aws4.group"
    assert attributes.get('grIcon') == "mxgraph.aws4.group_aws_cloud_alt"


@pytest.mark.parametrize('source, expected', [
    pytest.param({"mxfile": {"diagram": ['a', 'b']}}, True, id="is multiple page"),
    pytest.param({"mxfile": {"diagram": 'a'}}, False, id="is single page"),
])
def test_is_multiple_pages(source, expected):
    assert drawio_dict_utils.is_multiple_pages(source) == expected


def test_get_components_from_source():
    # GIVEN a DrawIO with one component and Dataflow with multiple configurations
    source = json.loads(get_byte_data(test_resource_paths.aws_two_component_multiple_dataflows))

    # WHEN drawio_dict_utils::get_components_from_source
    components = drawio_dict_utils.get_components_from_source(source)

    # THEN it returns a unique component
    assert len(components) == 2


def test_get_dataflows_from_source():
    # GIVEN a DrawIO with one component and Dataflow with multiple configurations
    source = json.loads(get_byte_data(test_resource_paths.aws_two_component_multiple_dataflows))

    # WHEN drawio_dict_utils::get_components_from_source
    dataflows = drawio_dict_utils.get_dataflows_from_source(source)

    # THEN it returns 5 dataflows
    assert len(dataflows) == 5
