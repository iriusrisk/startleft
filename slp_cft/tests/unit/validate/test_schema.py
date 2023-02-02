from unittest import TestCase

import yaml

from slp_base.slp_base.schema import Schema
from slp_cft import CloudformationMappingFileValidator
from slp_cft.tests.resources import test_resource_paths

SCHEMA_FILENAME = CloudformationMappingFileValidator.schema_filename
VALID_MAPPING_FILE = test_resource_paths.cloudformation_mapping_iriusrisk
INVALID_MAPPING_FILE = test_resource_paths.cloudformation_malformed_mapping_wrong_id


class TestSchema(TestCase):

    def test_valid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_cft', SCHEMA_FILENAME)
        mapping_file = VALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert mapping_file_schema.valid

    def test_invalid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_cft', SCHEMA_FILENAME)
        mapping_file = INVALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert not mapping_file_schema.valid
        assert mapping_file_schema.errors == "'id' is a required property"