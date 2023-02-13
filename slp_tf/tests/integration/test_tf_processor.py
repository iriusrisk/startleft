import pytest

from sl_util.sl_util.file_utils import get_data, get_byte_data
from slp_base.slp_base.errors import OTMBuildingError, MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_base.tests.util.otm import validate_and_compare
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import expected_aws_altsource_components, \
    expected_run_valid_mappings, expected_aws_parent_children_components, expected_aws_singleton_components, \
    expected_aws_security_groups_components, expected_mapping_skipped_component_without_parent, expected_no_resources, \
    expected_mapping_modules, expected_extra_modules, expected_elb_example, terraform_for_mappings_tests_json, \
    expected_separated_networks_components, terraform_iriusrisk_tf_aws_mapping, terraform_minimal_content_otm, \
    tf_components_with_trustzones_of_same_type_otm, tf_file_referenced_vars_expected_result, \
    minimal_otm_expected_result, otm_with_only_default_trustzone_expected_result, \
    terraform_iriusrisk_tf_aws_mapping_v180
from slp_tf.tests.resources.test_resource_paths import expected_orphan_component_is_not_mapped
from slp_tf.tests.utility import excluded_regex

PUBLIC_CLOUD_TZ_ID = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
INTERNET_TZ_ID = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
DEFAULT_TRUSTZONE_ID = "b61d6911-338d-46a8-9f39-8dcd24abfe91"

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_TF_FILE = terraform_for_mappings_tests_json


class TestTerraformProcessor:

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_orphan_component_is_not_mapped(self, mapping_file):
        # GIVEN a valid TF file with a resource (VPCssm) whose parents do (private VPCs) not exist in the file
        terraform_file = get_data(test_resource_paths.terraform_orphan_component)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the VPCsmm components without parents are omitted
        # AND the rest of the OTM details match the expected
        result, expected = validate_and_compare(otm.json(), expected_orphan_component_is_not_mapped, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_run_valid_mappings(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_for_mappings_tests_json)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_run_valid_mappings, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_aws_parent_children_components(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_parent_children_components)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_aws_parent_children_components, excluded_regex)
        assert result == expected

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

    def test_mapping_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_component_without_parent)

        # AND an invalid TF mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        # THEN an OTMBuildingError is raised
        with pytest.raises(OTMBuildingError) as e_info:
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
        result, expected = validate_and_compare(otm, expected_mapping_skipped_component_without_parent, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_no_resources(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_no_resources)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_no_resources, excluded_regex)
        assert result == expected

    def test_mapping_modules(self):
        # GIVEN a valid TF file with some TF modules
        terraform_file = get_data(test_resource_paths.terraform_modules)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_mapping_modules, excluded_regex)
        assert result == expected

    def test_extra_modules(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_extra_modules_sample)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_extra_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_extra_modules, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_elb_example(self, mapping_file):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_elb)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_elb_example, excluded_regex)
        assert result == expected

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
        mapping_file = [get_data(terraform_iriusrisk_tf_aws_mapping)]

        # When creating OTM project from IaC file
        # Then raises OTMBuildingError
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_expected_separated_networks_components(self, mapping_file):
        # GIVEN the single tf file with all the resources
        single_file = get_data(test_resource_paths.terraform_single_tf)

        # AND the same resources separated in two files
        networks = get_data(test_resource_paths.terraform_networks)
        resources = get_data(test_resource_paths.terraform_resources)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(mapping_file)

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
    def test_iac_file_is_invalid(self, source):
        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN creating OTM project from IaC file
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, source, [mapping_file]).process()

    def test_minimal_tf_file(self):
        # Given a minimal valid TF file
        terraform_minimal_file = get_data(test_resource_paths.terraform_minimal_content)

        # and the default mapping file for TF
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # When parsing the file with Startleft and the default mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_minimal_file], [mapping_file]).process()

        # Then an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(), otm_with_only_default_trustzone_expected_result,
                                                    excluded_regex)
        assert result == expected

    def test_generate_empty_otm_with_empty_mapping_file(self):
        # Given an empty mapping file
        mapping_file = get_data(test_resource_paths.empty_terraform_mapping)

        # and a valid TF file with content
        terraform_file = get_data(test_resource_paths.terraform_aws_simple_components)

        # When parsing the file with Startleft and the empty mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # Then an empty OTM, without any threat modeling content, is generated
        result, expected = validate_and_compare(otm.json(), minimal_otm_expected_result, excluded_regex)
        assert result == expected

    def test_variable_references_in_tfvars_file_processed_ok(self):
        # GIVEN the multiples tf file and tfvars file
        terraform_main = get_data(test_resource_paths.terraform_main_referenced_variables)
        terraform_vars = get_data(test_resource_paths.terraform_variables_file_referenced_variables)
        terraform_referenced_vars = get_data(test_resource_paths.terraform_vars_referenced_variables)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [terraform_main, terraform_vars, terraform_referenced_vars], [mapping_file]
        ).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        result, expected = validate_and_compare(otm.json(), tf_file_referenced_vars_expected_result,
                                 excluded_regex)
        assert result == expected

    def test_security_group_components_from_same_resource(self):
        # GIVEN a valid TF file with a security group containing both an inbound and an outbound rule
        tf_file = get_data(test_resource_paths.terraform_components_from_same_resource)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

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

    def test_resources_with_same_name(self):
        """
        Generate an OTM for TF file with resources with the same name
        """

        # GIVEN a TF file with two resources of different types and the same name id
        #    AND the default mapping file
        tf_file = get_data(test_resource_paths.terraform_resources_with_same_name)
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND both components are mapped with the same name
        assert len(otm.components) == 2
        assert otm.components[0].name == otm.components[1].name

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(terraform_iriusrisk_tf_aws_mapping), id="with actual mapping file"),
        pytest.param(get_data(terraform_iriusrisk_tf_aws_mapping_v180), id="with backwards mapping_file")])
    def test_aws_security_groups_components_full_example(self, mapping_file):
        """
        Test backward compatibility of aws_security_groups_components.tf
        against iriusrisk-tf-aws-mapping-1.8.0 mapping file (release 1.8.0)
        """
        # GIVEN the TF file of aws security groups
        # AND a valid mapping file
        terraform_file = get_data(test_resource_paths.terraform_aws_security_groups_components)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        #   AND backward compatibility works correctly
        result, expected = validate_and_compare(otm, expected_aws_security_groups_components, excluded_regex)
        assert result == expected

    def test_trustzone_types(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_minimal_content)

        # AND a valid TF mapping file that defines two TZs, one with type and the one without type
        mapping_file = get_data(test_resource_paths.terraform_trustzone_types_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(), terraform_minimal_content_otm, None)
        assert result == expected

    def test_components_with_trustzones_of_same_type(self):
        # GIVEN a valid TF file WITH some components mapped to different TZs of the same type
        terraform_file = get_data(test_resource_paths.terraform_components_with_trustzones_of_same_type)

        # AND a valid TF mapping file that defines two different TZs of the same type
        mapping_file = get_data(test_resource_paths.terraform_multiple_trustzones_same_type_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(), tf_components_with_trustzones_of_same_type_otm, None)
        assert result == expected
