from unittest import TestCase

from startleft.api.errors import MappingFileNotValidError
from startleft.processors.base.mapping import MultipleMappingFileValidator, MappingFileValidator
from tests.resources.test_resource_paths import *


class TestMapping(TestCase):

    def test_multiple_mapping_file_validator(self):
        mapping_file_schema = 'etm_mapping_schema.json'
        mapping_file = mtmt_empty_mapping_file

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        try:
            MultipleMappingFileValidator(mapping_file_schema, [mapping_file_data]).validate()
        except Exception as e:
            self.fail(e)

    def test_mapping_file_validator(self):
        mapping_file_schema = 'etm_mapping_schema.json'
        mapping_file = mtmt_empty_mapping_file

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        try:
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()
        except Exception as e:
            self.fail("Unexpected exception " + e.__str__())

    def test_mapping_file_validator_invalid_schema(self):
        mapping_file_schema = 'etm_mapping_schema.json'
        mapping_file = default_terraform_mapping

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        with self.assertRaises(MappingFileNotValidError):
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()

    def test_mapping_file_validator_invalid_size(self):
        mapping_file_schema = 'etm_mapping_schema.json'
        mapping_file = empty_mapping_file

        with open(mapping_file) as file:
            mapping_file_data = file.read()

        with self.assertRaises(MappingFileNotValidError):
            MappingFileValidator(mapping_file_schema, mapping_file_data).validate()