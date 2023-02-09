from pytest import mark, param

from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import validate_and_compare
from slp_tf import TerraformProcessor
from slp_tf.tests.integration.test_tf_processor import VALIDATION_EXCLUDED_REGEX
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping, \
    expected_aws_singleton_components

TERRAFORM_FOR_CATCHALL_TESTS = test_resource_paths.terraform_for_catchall_tests
TERRAFORM_ONLY_CATCHALL_MAPPING = test_resource_paths.tf_only_catchall
TERRAFORM_ONLY_CATCHALL_EXPECTED = test_resource_paths.tf_expected_only_catchall
TERRAFORM_EXPLICIT_MAPPING_AND_CATCHALL_MAPPING = test_resource_paths.tf_explicit_mapping_and_catchall
TERRAFORM_EXPLICIT_MAPPING_AND_CATCHALL_EXPECTED = test_resource_paths.tf_expected_explicit_mapping_and_catchall
TERRAFORM_SKIP_AND_CATCHALL_MAPPING = test_resource_paths.tf_skip_and_catchall
TERRAFORM_SKIP_AND_CATCHALL_EXPECTED = test_resource_paths.tf_expected_skip_and_catchall
TERRAFORM_SINGLETON_AND_CATCHALL_MAPPING = test_resource_paths.tf_singleton_and_catchall
TERRAFORM_SINGLETON_AND_CATCHALL_EXPECTED = test_resource_paths.tf_expected_singleton_and_catchall

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformMappingFunctions:

    @mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_aws_singleton_components(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_singleton_components_unix_line_breaks)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        actual, expected = validate_and_compare(otm, expected_aws_singleton_components, VALIDATION_EXCLUDED_REGEX)
        assert actual == expected

    def test_aws_ip_unified_components(self):
        """
        Generate an OTM with multiple components unified by $ip
        """
        # GIVEN a TF file with two resources
        #   AND a mapping file maps those resources by $ip
        #   AND the $ip value is assigned to the same value
        tf_file = get_data(test_resource_paths.terraform_multiple_aws_security_group)
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND a unique component is generated
        assert len(otm.components) == 1
        assert otm.components[0].name == '0.0.0.0/0'
        assert otm.components[0].type == 'generic-client'

    def test_aws_ip_unique_resource_multiple_mappings(self):
        """
        Generate an OTM with a unique resource multiplied using $ip mapping
        """
        # GIVEN a TF file with one resource
        #   AND a mapping file map multiple times resources by $ip
        #   AND the $ip value is assigned to a distinct value
        tf_file = get_data(test_resource_paths.terraform_aws_security_group_in_and_eg_gress)
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND two components are generated
        assert len(otm.components) == 2
        assert otm.components[0].name == '192.168.0.1/0'
        assert otm.components[0].type == 'generic-client'

        assert otm.components[1].name == '0.0.0.0/0'
        assert otm.components[1].type == 'generic-client'

    @mark.parametrize('mapping_file,expected_otm', [
        # Only catchall
        param(TERRAFORM_ONLY_CATCHALL_MAPPING, TERRAFORM_ONLY_CATCHALL_EXPECTED, id='only_catchall'),
        # Explicit mapping and catchall
        param(TERRAFORM_EXPLICIT_MAPPING_AND_CATCHALL_MAPPING, TERRAFORM_EXPLICIT_MAPPING_AND_CATCHALL_EXPECTED,
              id='explicit_mapping_and_catchall'),
        # Skip and catchall
        param(TERRAFORM_SKIP_AND_CATCHALL_MAPPING, TERRAFORM_SKIP_AND_CATCHALL_EXPECTED, id='skip_and_catchall'),
        # Singleton and catchall
        param(TERRAFORM_SINGLETON_AND_CATCHALL_MAPPING, TERRAFORM_SINGLETON_AND_CATCHALL_EXPECTED,
              id='singleton_and_catchall')])
    def test_aws_catchall_components(self, mapping_file, expected_otm):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(TERRAFORM_FOR_CATCHALL_TESTS)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM matches the expected one
        actual, expected = validate_and_compare(otm, expected_otm, VALIDATION_EXCLUDED_REGEX)
        assert actual == expected
