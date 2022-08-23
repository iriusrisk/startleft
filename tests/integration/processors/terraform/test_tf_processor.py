import pytest

from startleft.api.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError
from startleft.processors.terraform.tf_processor import TerraformProcessor
from startleft.utils.file_utils import get_data
from tests.resources import test_resource_paths
from tests.util import otm as utils

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_TF_FILE = test_resource_paths.terraform_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.default_terraform_aws_mapping


class TestTerraformProcessor:

    def test_run_valid_mappings(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_for_mappings_tests_json)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'

        assert otm.components[0].type == 'vpc'
        assert otm.components[0].name == 'vpc'
        assert otm.components[0].parent_type == 'trustZone'

        assert otm.components[1].type == 'ec2'
        assert otm.components[1].name == 'inst'
        assert otm.components[1].parent_type == 'trustZone'

        assert otm.components[2].type == 'empty-component'
        assert otm.components[2].name == 'subnet_1'
        assert otm.components[2].parent_type == 'component'

        assert otm.components[3].type == 'empty-component'
        assert otm.components[3].name == 'subnet_2'
        assert otm.components[3].parent_type == 'component'

    def test_mapping_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_component_without_parent)

        # AND an invalid TF mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        # THEN an OtmBuildingError is raised
        with pytest.raises(OtmBuildingError) as e_info:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # AND the error references a parent issue
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    def test_mapping_skipped_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_skipped_component_without_parent)

        # AND a TF mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 1
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'
        assert otm.components[0].type == 'aws_control'
        assert otm.components[0].name == 'Control_component'
        assert otm.components[0].parent == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

    def test_no_resources(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_no_resources)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'

    def test_mapping_modules(self):
        # GIVEN a valid TF file with some TF modules
        terraform_file = get_data(test_resource_paths.terraform_modules)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        aws_rds_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/rds/aws')
        assert aws_rds_modules[0].name == 'db23test'
        assert aws_rds_modules[0].parent_type == 'trustZone'
        assert aws_rds_modules[0].source['source'] == 'terraform-aws-modules/rds/aws'

    def test_extra_modules(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_extra_modules_sample)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_extra_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        rds_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/rds/aws')
        vpc_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/vpc/aws')
        load_balancer_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/alb/aws')

        assert len(rds_modules) == 1
        assert len(vpc_modules) == 1
        assert len(load_balancer_modules) == 1

        assert rds_modules[0].source['source'] == 'terraform-aws-modules/rds/aws'
        assert vpc_modules[0].source['source'] == 'terraform-aws-modules/vpc/aws'
        assert load_balancer_modules[0].source['source'] == 'terraform-aws-modules/alb/aws'

    @pytest.mark.parametrize('mapping_file', [None, [None]])
    def test_mapping_files_not_provided(self, mapping_file):
        # GIVEN a sample valid IaC file (and none mapping file)
        terraform_file = [get_data(SAMPLE_VALID_TF_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises TypeError
        with pytest.raises(TypeError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, [get_data(mapping_file)]).process()

    def test_invalid_mapping_files(self):
        # GIVEN a sample valid IaC file
        terraform_file = get_data(SAMPLE_VALID_TF_FILE)

        # AND an invalid iac mappings file
        mapping_file = [get_data(test_resource_paths.invalid_yaml)]

        # WHEN creating OTM project from IaC file
        # THEN raises MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, mapping_file).process()

    def test_invalid_terraform_file(self):
        # Given a sample invalid TF file
        terraform_file = [get_data(test_resource_paths.invalid_tf)]

        # And a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # When creating OTM project from IaC file
        # Then raises OtmBuildingError
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_file, mapping_file).process()

