import pytest

from sl_util.sl_util.file_utils import get_data
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping, \
    expected_aws_singleton_components, expected_aws_altsource_components
from slp_tf.tests.utility import excluded_regex
from slp_base.tests.util.otm import validate_and_compare

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformMappingFunctions:

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_aws_singleton_components(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_singleton_components_unix_line_breaks)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_aws_singleton_components, excluded_regex)
        assert result == expected

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

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_aws_altsource_components(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_altsource_components)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_aws_altsource_components, excluded_regex)
        assert result == expected
