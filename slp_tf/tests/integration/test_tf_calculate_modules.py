from sl_util.sl_util.file_utils import get_data
from slp_tf.tests.resources import test_resource_paths
from slp_tf import TerraformProcessor
from slp_base.tests.util.otm import validate_and_compare
from slp_tf.tests.utility import excluded_regex

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformCalculateModules:

    def test_mapping_modules(self):
        # GIVEN a valid TF file with some TF modules
        terraform_file = get_data(test_resource_paths.terraform_modules)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, test_resource_paths.expected_mapping_modules, excluded_regex)
        assert result == expected

    def test_extra_modules(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_extra_modules_sample)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_extra_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, test_resource_paths.expected_extra_modules, excluded_regex)
        assert result == expected
