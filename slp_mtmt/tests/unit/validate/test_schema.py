from unittest import TestCase

import yaml

from slp_base.slp_base.schema import Schema
from slp_mtmt.slp_mtmt.mtmt_mapping_file_validator import MTMTMappingFileValidator
from slp_mtmt.tests.resources import test_resource_paths

SCHEMA_FILENAME = MTMTMappingFileValidator.schema_filename
VALID_MAPPING_FILE = test_resource_paths.mtmt_default_mapping
INVALID_MAPPING_FILE = test_resource_paths.mtmt_mapping_invalid_no_dataflows


class TestSchema(TestCase):

    def test_valid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_mtmt', SCHEMA_FILENAME)
        mapping_file = VALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert mapping_file_schema.valid

    def test_invalid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_mtmt', SCHEMA_FILENAME)
        mapping_file = INVALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert not mapping_file_schema.valid
        assert mapping_file_schema.errors == "'dataflows' is a required property"