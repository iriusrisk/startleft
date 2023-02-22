from unittest import TestCase

import yaml

from slp_base.slp_base.otm_validator import OTMValidator
from slp_base.slp_base.schema import Schema
from slp_base.tests.resources import test_resource_paths

SAMPLE_MAPPING_FILE = test_resource_paths.cft_mapping_no_dataflows
OTM_WITHOUT_VERSION = test_resource_paths.otm_without_version
CFT_MAPPING_SCHEMA = test_resource_paths.iac_cft_mapping_schema
OTM_SCHEMA_FILENAME = OTMValidator.schema_filename


class TestSchema(TestCase):

    def test_mapping_without_dataflows(self):
        mapping_file_schema = CFT_MAPPING_SCHEMA
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
        schema = Schema.from_package('otm', OTM_SCHEMA_FILENAME)

        # and an OTM without the “otmVersion” field
        otm = OTM_WITHOUT_VERSION

        with open(otm) as file:
            otm_file_content = file.read()

        otm_file_data = yaml.load(otm_file_content, Loader=yaml.BaseLoader)

        # when validating the OTM file against the schema
        schema.validate(otm_file_data)

        # then the OTM file is not valid
        assert not schema.valid


