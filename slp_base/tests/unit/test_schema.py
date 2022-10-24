from unittest import TestCase

import yaml

from slp_base.slp_base.schema import Schema
from slp_base.tests.resources import test_resource_paths

SAMPLE_MAPPING_FILE = test_resource_paths.cft_mapping_no_dataflows
OTM_WITHOUT_VERSION = test_resource_paths.otm_without_version


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

    def test_schema_validation_without_otm_version(self):
        # Given the Startleft’s OTM schema
        otm_file_schema = 'otm_schema.json'

        # and an OTM without the “otmVersion” field
        otm = OTM_WITHOUT_VERSION

        with open(otm) as file:
            otm_file_content = file.read()

        otm_file_data = yaml.load(otm_file_content, Loader=yaml.BaseLoader)

        # when validating the OTM file against the schema
        schema = Schema(otm_file_schema)
        schema.validate(otm_file_data)

        # then the OTM file is not valid
        assert not schema.valid


