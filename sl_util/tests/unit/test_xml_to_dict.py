import json
from unittest import TestCase

import pytest

from sl_util.sl_util.dict_utils import compare_dict
from sl_util.sl_util.file_utils import get_byte_data
from sl_util.sl_util.xml_to_dict import XmlToDict
from sl_util.tests.resources.test_resource_paths import random_data_xml, random_data_xml_json


class TestXmlToDict(TestCase):

    def test_to_dict(self):
        # GIVEN the source MTMT data
        xml = get_byte_data(random_data_xml).decode()
        # AND the parser
        parser = XmlToDict(xml)
        # AND the expected result
        expected_data = json.loads(get_byte_data(random_data_xml_json).decode())

        # WHEN we convert to json
        result_data = parser.to_dict()

        # THEN the result is as expected
        result, expected = compare_dict(result_data, expected_data)
        assert result == expected

    def test_to_dict_invalid_data(self):
        # GIVEN the source MTMT data
        xml = "INVALID XML CONTENT"
        # AND the parser
        parser = XmlToDict(xml)

        # WHEN we convert to json
        # THEN a ParseError is raised
        with pytest.raises(Exception) as error:
            parser.to_dict()
        # AND the error is as expected
        assert error.typename == 'ParseError'
        assert str(error.value.msg) == 'syntax error: line 1, column 0'
