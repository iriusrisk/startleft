import pytest

from startleft.api.controllers.iac.iac_type import IacType
from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


def assert_otm(otm, position, c_type, c_name, c_parent):
    assert otm.components[position].type == c_type
    assert otm.components[position].name == c_name
    assert otm.components[position].parent == c_parent


class TestTerraformAWSComponents:

    def test_aws_components_for_test(self):
        filename = test_resource_paths.terraform_aws_components_for_test
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test Case AWS components', 'aws_components_for_test', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-terraform.otm', filename)
        public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 18
        assert_otm(otm, 0, 'cloudtrail', 'foobar', public_cloud_id)
        assert_otm(otm, 1, 'cognito', 'main', public_cloud_id)
        assert_otm(otm, 2, 'cognito', 'pool', public_cloud_id)
        assert_otm(otm, 3, 'docker-container', 'service', public_cloud_id)
        assert_otm(otm, 4, 'docker-container', 'service_task', public_cloud_id)
        assert_otm(otm, 5, 'elastic-container-service', 'mongo', public_cloud_id)
        assert_otm(otm, 6, 'elastic-container-kubernetes', 'example', public_cloud_id)
        assert_otm(otm, 7, 'load-balancer', 'wu-tang', public_cloud_id)
        assert_otm(otm, 8, 'aws-lambda-function', 'test_lambda', public_cloud_id)
        assert_otm(otm, 9, 'CD-AWS-NETWORK-FIREWALL', 'firewall_example', public_cloud_id)
        assert_otm(otm, 10, 'rds', 'aurora-cluster-demo', public_cloud_id)
        assert_otm(otm, 11, 'redshift', 'tf-redshift-cluster', public_cloud_id)
        assert_otm(otm, 12, 'route-53', 'route-53-zone-example', public_cloud_id)
        assert_otm(otm, 13, 's3', 'foo_s3_bucket', public_cloud_id)
        assert_otm(otm, 14, 'sqs-simple-queue-service', 'terraform_queue', public_cloud_id)
        assert_otm(otm, 15, 'empty-component', 'some-canary', public_cloud_id)
        assert_otm(otm, 16, 'step-functions', 'my_sfn_state_machine', public_cloud_id)
        assert_otm(otm, 17, 'step-functions', 'my_sfn_activity', public_cloud_id)

    @pytest.mark.parametrize('filename', [
        test_resource_paths.terraform_aws_singleton_components_unix_line_breaks,
        [open(test_resource_paths.terraform_aws_singleton_components_unix_line_breaks, 'rb')],
        test_resource_paths.terraform_aws_singleton_components_dos_line_breaks,
        [open(test_resource_paths.terraform_aws_singleton_components_dos_line_breaks, 'rb')],
        test_resource_paths.terraform_aws_singleton_components_classic_macos_line_breaks,
        [open(test_resource_paths.terraform_aws_singleton_components_classic_macos_line_breaks, 'rb')]
    ])
    def test_aws_singleton_components(self, filename: str):
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS singleton components', 'aws_singleton_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-singleton-terraform.otm', filename)

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 20
        assert len(otm.dataflows) == 0
