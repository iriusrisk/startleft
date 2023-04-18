import pytest
from sl_util.sl_util.file_utils import get_byte_data
from slp_tf.tests.resources import test_resource_paths
from slp_tf import TerraformProcessor
from slp_base.tests.util.otm import validate_and_compare
from slp_tf.tests.utility import excluded_regex

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformCalculateSecurityGroups:

    def test_security_group_components_from_same_resource(self):
        # GIVEN a valid TF file with a security group containing both an inbound and an outbound rule
        tf_file = get_byte_data(test_resource_paths.terraform_components_from_same_resource)

        # AND a valid CFT mapping file
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the CFT file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        # AND the component IDs are differentiated by their IPs
        ingress_id = list(filter(lambda obj: obj.name == '52.30.97.44/32', otm.components))[0].id
        egress_id = list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))[0].id

        assert ingress_id != egress_id
        assert '52_30_97_44_32' in ingress_id
        assert '0_0_0_0_0' in egress_id

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping), id="with actual mapping file"),
        pytest.param(get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping_v180),
                     id="with backwards mapping_file")])
    def test_aws_security_groups_components_full_example(self, mapping_file):
        """
        Test backward compatibility of aws_security_groups_components.tf
        against iriusrisk-tf-aws-mapping-1.8.0 mapping file (release 1.8.0)
        """
        # GIVEN the TF file of aws security groups
        # AND a valid mapping file
        terraform_file = get_byte_data(test_resource_paths.terraform_aws_security_groups_components)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        #   AND backward compatibility works correctly
        result, expected = validate_and_compare(otm, test_resource_paths.expected_aws_security_groups_components,
                                                excluded_regex)
        assert result == expected
