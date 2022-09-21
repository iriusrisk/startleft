from unittest import TestCase

import yaml

from slp_base.slp_base.schema import Schema
from slp_base.tests.resources import test_resource_paths

SAMPLE_MAPPING_FILE = test_resource_paths.cft_mapping_no_dataflows


class TestSchema(TestCase):

    def test_mapping_without_dataflows(self):
        mapping_file_schema = 'iac_mapping_schema.json'
        mapping_file = SAMPLE_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.BaseLoader)

        schema = Schema(mapping_file_schema)
        schema.validate(mapping_file_data)

        assert not schema.valid
        assert schema.errors == "'dataflows' is a required property"

