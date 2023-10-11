import json
from tempfile import SpooledTemporaryFile
from unittest.mock import Mock, patch

from pytest import mark

from sl_util.sl_util.dict_utils import compare_dict
from sl_util.sl_util.file_utils import get_byte_data
from slp_drawio.slp_drawio.load.drawio_to_dict import DrawIOToDict
from slp_drawio.tests.resources.test_resource_paths import aws_minimal_drawio, aws_minimal_xml, \
    aws_minimal_drawio_as_json


class TestDrawioToDict:

    @patch('tempfile.SpooledTemporaryFile.read')
    @mark.parametrize('file,expected', [
        (aws_minimal_xml, aws_minimal_drawio_as_json),
        (aws_minimal_drawio, aws_minimal_drawio_as_json),
    ])
    def test_json(self, read_mock, file: str, expected: str):
        # GIVEN the mocked content
        read_mock.return_value = get_byte_data(file)
        # AND the parser
        parser = DrawIOToDict(Mock(file=SpooledTemporaryFile()))
        # AND the expected content as json
        expected_content = json.loads(get_byte_data(expected))

        # WHEN we get the json from the xml
        json_ = parser.to_dict()

        # THEN both json are the same
        exclude_paths = ["root['mxfile']['etag']", "root['mxfile']['modified']"]
        result_xml, result_64 = compare_dict(json_, expected_content, exclude_paths=exclude_paths)
        assert result_xml == result_64
