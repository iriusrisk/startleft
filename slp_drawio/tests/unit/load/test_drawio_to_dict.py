from typing import Dict
from unittest.mock import MagicMock, Mock

import pytest
from pytest import mark, param, fixture

from sl_util.sl_util.dict_utils import compare_dict
from sl_util.sl_util.file_utils import get_as_str, get_as_dict
from slp_drawio.slp_drawio.load.drawio_to_dict import DrawIOToDict, _get_file_content
from slp_drawio.tests.resources.test_resource_paths import aws_minimal_drawio, aws_minimal_xml, \
    aws_minimal_drawio_as_json


@mark.parametrize('content,expected', [
    param(b'something', 'something', id='right content'),
    param(b'', None, id='empty content'),
    param(None, None, id='no content'),
])
def test_get_file_content(content: str, expected):
    # GIVEN a mocked SpooledTemporaryFile read method
    def read_mock():
        return content

    file_mock = Mock(read=read_mock)

    # WHEN _get_file_content is invoked
    # THEN it returns the content of the file
    assert _get_file_content(file_mock) == expected


@fixture(autouse=True)
def read_mock(mocker, content):
    mocker.patch('slp_drawio.slp_drawio.load.drawio_to_dict._get_file_content', side_effect=[content])


class TestDrawioToDict:

    @mark.parametrize('content, error_type, error_msg', [
        param('INVALID XML CONTENT', 'ParseError', 'syntax error: line 1, column 0', id='no_xml'),
        param('<mxfile><diagram>7VbbcpswEP</diagram></mxfile>',
              'Error', 'Incorrect padding',
              id='alphanumeric_no_b64'),
        param('<mxfile><diagram>\x00\x00\x1C\x0A</diagram></mxfile>',
              'ParseError', 'not well-formed (invalid token): line 1, column 17',
              id='binary_no_64'),
        param('<mxfile><diagram>QkFTRTY0IEVOQ09ERUQgVVNFTEVTUyBDT05URU5UIA==</diagram></mxfile>',
              'error', 'Error -3 while decompressing data: invalid distance too far back',
              id='valid_b64_but_invalid_content'),
    ])
    def test_invalid_xml(self, read_mock, content, error_type, error_msg):
        # GIVEN the mocked content

        # WHEN DrawIOToDict::to_dict
        # THEN a ParseError is raised
        with pytest.raises(BaseException) as error:
            DrawIOToDict(MagicMock()).to_dict()
        # AND the error is as expected
        assert error.typename == error_type
        assert str(error.value) == error_msg

    @mark.parametrize('content,expected', [
        param(get_as_str(aws_minimal_xml), get_as_dict(aws_minimal_drawio_as_json), id='valid drawio'),
        param(get_as_str(aws_minimal_drawio), get_as_dict(aws_minimal_drawio_as_json), id='valid xml'),
        param(None, {}, id='no content')
    ])
    def test_correct_source(self, read_mock, content, expected: Dict):
        # GIVEN the mocked content

        # AND the parser
        parser = DrawIOToDict(MagicMock())

        # WHEN we get the source as dict from the xml
        source_dict = parser.to_dict()

        # THEN both are the same
        exclude_paths = ["root['mxfile']['etag']", "root['mxfile']['modified']"]
        result_xml, result_64 = compare_dict(source_dict, expected, exclude_paths=exclude_paths)
        assert result_xml == result_64
