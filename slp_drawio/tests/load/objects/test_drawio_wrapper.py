import json

from pytest import mark

from sl_util.sl_util.dict_utils import compare_dict
from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load.objects.drawio_wrapper import DrawioWrapper
from slp_drawio.tests.resources.test_resource_paths import aws_minimal_drawio, aws_minimal_xml, \
    aws_minimal_drawio_as_json


class TestDrawioWrapper:

    @mark.parametrize('source,expected', [
        (aws_minimal_xml, aws_minimal_drawio_as_json),
        (aws_minimal_drawio, aws_minimal_drawio_as_json),
    ])
    def test_json(self, source: str, expected: str):
        # GIVEN a xml exported drawio
        content = get_byte_data(source)
        # AND the expected content as json
        expected_content = json.loads(get_byte_data(expected))
        # AND the wrapper
        wrapper = DrawioWrapper(content)

        # WHEN we get the json from the xml
        json_ = wrapper.json()

        # THEN both json are the same
        exclude_paths = ["root['mxfile']['etag']", "root['mxfile']['modified']"]
        result_xml, result_64 = compare_dict(json_, expected_content, exclude_paths=exclude_paths)
        assert result_xml == result_64
