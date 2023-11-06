import json
from unittest import TestCase

from sl_util.sl_util.dict_utils import compare_dict
from sl_util.sl_util.file_utils import get_byte_data
from slp_mtmt.slp_mtmt.tm7_to_dict import Tm7ToDict
from slp_mtmt.tests.resources.test_resource_paths import model_mtmt_source_file, model_mtmt_source_file_otm


class TestTm7ToDict(TestCase):

    def test_to_dict(self):
        # GIVEN the source MTMT data
        xml = get_byte_data(model_mtmt_source_file).decode()

        # AND the expected content as json
        expected_content = json.loads(get_byte_data(model_mtmt_source_file_otm))

        # AND the parser
        parser = Tm7ToDict(xml)

        # WHEN we convert to json
        dict_ = parser.to_dict()

        # THEN dict is as expected
        result, expected = compare_dict(dict_, expected_content)
        assert result == expected
