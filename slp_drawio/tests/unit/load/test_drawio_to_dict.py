import json
from tempfile import SpooledTemporaryFile
from unittest.mock import Mock, patch

import pytest
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
    def test_correct_source(self, read_mock, file: str, expected: str):
        # GIVEN the mocked content
        read_mock.return_value = get_byte_data(file)
        # AND the parser
        parser = DrawIOToDict(Mock(file=SpooledTemporaryFile()))
        # AND the expected content as dict
        expected_content = json.loads(get_byte_data(expected))

        # WHEN we get the source as dict from the xml
        source_dict = parser.to_dict()

        # THEN both are the same
        exclude_paths = ["root['mxfile']['etag']", "root['mxfile']['modified']"]
        result_xml, result_64 = compare_dict(source_dict, expected_content, exclude_paths=exclude_paths)
        assert result_xml == result_64

    @patch('tempfile.SpooledTemporaryFile.read')
    @mark.parametrize('content, error_type, error_msg', [
        pytest.param(b'INVALID XML CONTENT', 'ParseError', 'syntax error: line 1, column 0', id='no_xml'),
        pytest.param(b'<mxfile><diagram>7VbbcpswEP</diagram></mxfile>',
                     'Error', 'Incorrect padding',
                     id='alphanumeric_no_b64'),
        pytest.param(b'<mxfile><diagram>\x00\x00\x1C\x0A</diagram></mxfile>',
                     'ParseError', 'not well-formed (invalid token): line 1, column 17',
                     id='binary_no_64'),
        pytest.param(b'<mxfile><diagram>QkFTRTY0IEVOQ09ERUQgVVNFTEVTUyBDT05URU5UIA==</diagram></mxfile>',
                     'error', 'Error -3 while decompressing data: invalid distance too far back',
                     id='valid_b64_but_invalid_content'),
    ])
    def test_invalid_xml(self, read_mock, content, error_type, error_msg):
        # GIVEN the mocked content
        read_mock.return_value = content

        # WHEN we initialize the parser
        # THEN a ParseError is raised
        with pytest.raises(BaseException) as error:
            DrawIOToDict(Mock(file=SpooledTemporaryFile()))
        # AND the error is as expected
        assert error.typename == error_type
        assert str(error.value) == error_msg
