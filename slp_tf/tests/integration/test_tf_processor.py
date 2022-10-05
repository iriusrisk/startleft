import pytest

from sl_util.sl_util.file_utils import get_data, get_byte_data
from slp_base.slp_base.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths

from slp_base.tests.util.otm import validate_and_diff as validate_and_diff_otm
from slp_tf.tests.resources.test_resource_paths import expected_aws_dataflows, expected_aws_altsource_components, \
    expected_run_valid_mappings, expected_aws_parent_children_components, expected_aws_singleton_components, \
    expected_aws_security_groups_components, expected_mapping_skipped_component_without_parent, expected_no_resources, \
    expected_mapping_modules, expected_extra_modules, expected_elb_example, terraform_for_mappings_tests_json, \
    default_terraform_aws_mapping

VALIDATION_EXCLUDED_REGEX = r"root\[\'dataflows'\]\[.+?\]\['id'\]"

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_TF_FILE = terraform_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = default_terraform_aws_mapping


class TestTerraformProcessor:

    def test_run_valid_mappings(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_for_mappings_tests_json)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_run_valid_mappings, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_dataflows(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_dataflows)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_aws_dataflows, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_parent_children_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_parent_children_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_aws_parent_children_components, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_singleton_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_singleton_components_unix_line_breaks)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_aws_singleton_components, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_altsource_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_altsource_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_aws_altsource_components, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_security_groups_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_security_groups_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_aws_security_groups_components, VALIDATION_EXCLUDED_REGEX) == {}

    def test_mapping_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_component_without_parent)

        # AND an invalid TF mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        # THEN an OtmBuildingError is raised
        with pytest.raises(OtmBuildingError) as e_info:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # AND the error references a parent issue
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    def test_mapping_skipped_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_skipped_component_without_parent)

        # AND a TF mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_mapping_skipped_component_without_parent, VALIDATION_EXCLUDED_REGEX) == {}

    def test_no_resources(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_no_resources)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_no_resources, VALIDATION_EXCLUDED_REGEX) == {}

    def test_mapping_modules(self):
        # GIVEN a valid TF file with some TF modules
        terraform_file = get_data(test_resource_paths.terraform_modules)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_mapping_modules, VALIDATION_EXCLUDED_REGEX) == {}

    def test_extra_modules(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_extra_modules_sample)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_extra_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_extra_modules, VALIDATION_EXCLUDED_REGEX) == {}

    def test_elb_example(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_elb)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff_otm(otm.json(), expected_elb_example, VALIDATION_EXCLUDED_REGEX) == {}

    @pytest.mark.parametrize('mapping_file', [None, [None]])
    def test_mapping_files_not_provided(self, mapping_file):
        # GIVEN a sample valid IaC file (and none mapping file)
        terraform_file = [get_data(SAMPLE_VALID_TF_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises TypeError
        with pytest.raises(TypeError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [get_data(mapping_file)]).process()

    def test_invalid_mapping_files(self):
        # GIVEN a sample valid IaC file
        terraform_file = get_data(SAMPLE_VALID_TF_FILE)

        # AND an invalid iac mappings file
        mapping_file = [get_data(test_resource_paths.invalid_yaml)]

        # WHEN creating OTM project from IaC file
        # THEN raises MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    def test_invalid_terraform_file(self):
        # Given a sample invalid TF file
        terraform_file = [get_data(test_resource_paths.invalid_tf)]

        # And a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # When creating OTM project from IaC file
        # Then raises OtmBuildingError
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    # Parse a Simple IaC file
    def test_process_single_tf_file(self):
        # GIVEN the single tf file
        terraform_file = get_data(test_resource_paths.terraform_single_tf)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        assert validate_and_diff_otm(otm.json(), test_resource_paths.tf_file_expected_result, VALIDATION_EXCLUDED_REGEX) == {}

    # Parse a Multiple IaC file
    def test_process_multiple_tf_file(self):
        # GIVEN the multiples tf file
        terraform_networks = get_data(test_resource_paths.terraform_networks)
        terraform_resources = get_data(test_resource_paths.terraform_resources)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [terraform_networks, terraform_resources], [mapping_file]
        ).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        assert validate_and_diff_otm(otm.json(), test_resource_paths.tf_file_expected_result, VALIDATION_EXCLUDED_REGEX) == {}

    # Parse an empty Array IaC file
    def test_process_empty_source_file_array(self):
        # GIVEN an empty array IaC file
        terraform_empty_iac_array = []

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(LoadingIacFileError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_empty_iac_array, [mapping_file]).process()

    @pytest.mark.parametrize('source', [
        # GIVEN a request with one iac_file keys with no value
        [get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with all iac_file keys with no value
        [get_data(test_resource_paths.terraform_invalid_size),
         get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with no value
        [get_data(test_resource_paths.terraform_single_tf),
         get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with invalid format
        [get_data(test_resource_paths.terraform_single_tf),
         get_byte_data(test_resource_paths.terraform_gz)]
    ])
    def test_mapping_files_not_provided(self, source):
        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN creating OTM project from IaC file
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, source, [mapping_file]).process()
