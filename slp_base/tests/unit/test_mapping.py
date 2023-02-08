from unittest import TestCase

from slp_base import MappingFileNotValidError
from slp_base import MultipleMappingFileValidator, MappingFileValidator
from slp_base.slp_base.schema import Schema
from slp_base.tests.resources import test_resource_paths

SAMPLE_MAPPING_FILE = test_resource_paths.mtmt_mapping_file
ETM_MAPPING_SCHEMA = test_resource_paths.etm_mapping_schema
IAC_CFT_MAPPING_SCHEMA = test_resource_paths.iac_cft_mapping_schema


class TestMapping(TestCase):

    def test_multiple_mapping_file_validator(self):
        mapping_file_schema = Schema(ETM_MAPPING_SCHEMA)
        mapping_file = SAMPLE_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        try:
            MultipleMappingFileValidator(mapping_file_schema, [mapping_file_data]).validate()
        except Exception as e:
            self.fail(e)

    def test_mapping_file_validator(self):
        mapping_file_schema = Schema(ETM_MAPPING_SCHEMA)
        mapping_file = SAMPLE_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        try:
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()
        except Exception as e:
            self.fail("Unexpected exception " + e.__str__())

    def test_mapping_file_validator_invalid_schema(self):
        mapping_file_schema = Schema(ETM_MAPPING_SCHEMA)
        mapping_file = test_resource_paths.tf_mapping

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        with self.assertRaises(MappingFileNotValidError):
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()

    def test_mapping_file_validator_invalid_size(self):
        mapping_file_schema = Schema(ETM_MAPPING_SCHEMA)
        mapping_file = test_resource_paths.empty_mapping_file

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        with self.assertRaises(MappingFileNotValidError):
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()

    def test_invalid_mapping_file(self):
        # Given the iac terraform schema
        mapping_file_schema = Schema(IAC_CFT_MAPPING_SCHEMA)

        # And a malformed mapping file
        mapping_file_data = 'CFT NOT VALID Description: \n' \
                            '(SO0111) AWS Security Hub, v1.3.1 \n' \
                            'AWSTemplateFormatVersion: "2010-09-09'

        # And the mapping validator instance
        validator = MultipleMappingFileValidator(mapping_file_schema, [mapping_file_data])

        # When we validate the mapping file
        # Then we get a validation error
        self.assertRaises(MappingFileNotValidError, validator.validate)
