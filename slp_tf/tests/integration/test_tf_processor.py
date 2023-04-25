import pytest

from sl_util.sl_util.file_utils import get_byte_data
from slp_base.slp_base.errors import MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_base.tests.util.otm import validate_and_compare
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import \
    expected_run_valid_mappings, expected_elb_example, terraform_for_mappings_tests_json, \
    expected_separated_networks_components, terraform_iriusrisk_tf_aws_mapping, \
    tf_file_referenced_vars_expected_result, \
    minimal_otm_expected_result, otm_with_only_default_trustzone_expected_result, expected_no_resources
from slp_tf.tests.utility import excluded_regex

PUBLIC_CLOUD_TZ_ID = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
INTERNET_TZ_ID = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
DEFAULT_TRUSTZONE_ID = "b61d6911-338d-46a8-9f39-8dcd24abfe91"

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_TF_FILE = terraform_for_mappings_tests_json


class TestTerraformProcessor:

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_run_valid_mappings(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_byte_data(test_resource_paths.terraform_for_mappings_tests_json)

        # AND a valid TF mapping file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_run_valid_mappings, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_no_resources(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_byte_data(test_resource_paths.terraform_no_resources)

        # AND a valid TF mapping file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_no_resources, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_elb_example(self, mapping_file):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_byte_data(test_resource_paths.terraform_elb)

        # AND a valid TF mapping file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_elb_example, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [None, [None]])
    def test_mapping_files_not_provided(self, mapping_file):
        # GIVEN a sample valid IaC file (and none mapping file)
        terraform_file = [get_byte_data(SAMPLE_VALID_TF_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises TypeError
        with pytest.raises(TypeError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [get_byte_data(mapping_file)]).process()

    def test_invalid_mapping_files(self):
        # GIVEN a sample valid IaC file
        terraform_file = get_byte_data(SAMPLE_VALID_TF_FILE)

        # AND an invalid iac mappings file
        mapping_file = [get_byte_data(test_resource_paths.invalid_yaml)]

        # WHEN creating OTM project from IaC file
        # THEN raises MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    def test_invalid_terraform_file(self):
        # Given a sample invalid TF file
        terraform_file = [get_byte_data(test_resource_paths.invalid_tf)]

        # And a valid iac mappings file
        mapping_file = [get_byte_data(terraform_iriusrisk_tf_aws_mapping)]

        # When creating OTM project from IaC file
        # Then raises OTMBuildingError
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_expected_separated_networks_components(self, mapping_file):
        # GIVEN the single tf file with all the resources
        single_file = get_byte_data(test_resource_paths.terraform_single_tf)

        # AND the same resources separated in two files
        networks = get_byte_data(test_resource_paths.terraform_networks)
        resources = get_byte_data(test_resource_paths.terraform_resources)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the method TerraformProcessor::process is invoked for the single file
        otm_single = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [single_file], [mapping_file]
        ).process()

        # AND the method TerraformProcessor::process is invoked for the multiple files
        otm_multiple = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [networks, resources], [mapping_file]
        ).process()

        # THEN both generated OTMs are valid and equal
        result, expected = validate_and_compare(otm_single, otm_multiple, excluded_regex)
        assert result == expected

        # AND their content is the expected
        result, expected = validate_and_compare(otm_single, expected_separated_networks_components, excluded_regex)
        assert result == expected

    def test_process_empty_source_file_array(self):
        # GIVEN an empty array IaC file
        terraform_empty_iac_array = []

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(LoadingIacFileError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_empty_iac_array, [mapping_file]).process()

    @pytest.mark.parametrize('source', [
        # GIVEN a request with one iac_file keys with no value
        [get_byte_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with all iac_file keys with no value
        [get_byte_data(test_resource_paths.terraform_invalid_size),
         get_byte_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with no value
        [get_byte_data(test_resource_paths.terraform_single_tf),
         get_byte_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with invalid format
        [get_byte_data(test_resource_paths.terraform_single_tf),
         get_byte_data(test_resource_paths.terraform_gz)]
    ])
    def test_iac_file_is_invalid(self, source):
        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN creating OTM project from IaC file
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, source, [mapping_file]).process()

    def test_minimal_tf_file(self):
        # Given a minimal valid TF file
        terraform_minimal_file = get_byte_data(test_resource_paths.terraform_minimal_content)

        # and the default mapping file for TF
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # When parsing the file with Startleft and the default mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_minimal_file], [mapping_file]).process()

        # Then an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(), otm_with_only_default_trustzone_expected_result,
                                                excluded_regex)
        assert result == expected

    def test_generate_empty_otm_with_empty_mapping_file(self):
        # Given an empty mapping file
        mapping_file = get_byte_data(test_resource_paths.empty_terraform_mapping)

        # and a valid TF file with content
        terraform_file = get_byte_data(test_resource_paths.terraform_aws_simple_components)

        # When parsing the file with Startleft and the empty mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # Then an empty OTM, without any threat modeling content, is generated
        result, expected = validate_and_compare(otm.json(), minimal_otm_expected_result, excluded_regex)
        assert result == expected

    def test_variable_references_in_tfvars_file_processed_ok(self):
        # GIVEN the multiples tf file and tfvars file
        terraform_main = get_byte_data(test_resource_paths.terraform_main_referenced_variables)
        terraform_vars = get_byte_data(test_resource_paths.terraform_variables_file_referenced_variables)
        terraform_referenced_vars = get_byte_data(test_resource_paths.terraform_vars_referenced_variables)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [terraform_main, terraform_vars, terraform_referenced_vars], [mapping_file]
        ).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        result, expected = validate_and_compare(otm.json(), tf_file_referenced_vars_expected_result,
                                                excluded_regex)
        assert result == expected

    def test_resources_with_same_name(self):
        """
        Generate an OTM for TF file with resources with the same name
        """

        # GIVEN a TF file with two resources of different types and the same name id
        #    AND the default mapping file
        tf_file = get_byte_data(test_resource_paths.terraform_resources_with_same_name)
        mapping_file = get_byte_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND both components are mapped with the same name
        assert len(otm.components) == 2
        assert otm.components[0].name == otm.components[1].name

    def test_valid_terraform_size_over_1mb(self):

        # GIVEN a terraform file file under 2MB
        tf_file = get_data(test_resource_paths.terraform_invalid_size_over_1mb)
        # AND the default terraform mapping file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN processing
        # THEN a 400 error is returned
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, tf_file, [mapping_file]).process()
