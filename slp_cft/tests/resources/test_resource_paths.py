import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'

# mapping
default_cloudformation_mapping = path + '/mapping/cloudformation_mapping.yaml'
cloudformation_mapping_component_without_parent = path + '/mapping/cloudformation_mapping_component_without_parent.yaml'
cloudformation_mapping_all_functions = path + '/mapping/cloudformation_mapping_all_functions.yaml'
cloudformation_for_security_groups_mapping = path + \
                                             '/mapping/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_malformed_mapping_wrong_id = path + '/mapping/cloudformation_malformed_mapping_wrong_id.yaml'
cloudformation_mapping_iriusrisk = path + '/mapping/iriusrisk-cft-mapping.yaml'
cloudformation_mapping_without_ref = path + '/mapping/iriusrisk-cft-mapping_without_ref.yaml'
empty_cloudformation_mapping = path + '/mapping/empty_cloudformation_mapping.yaml'
cloudformation_trustzone_types_mapping = path + '/mapping/cloudformation_trustzone_types_mapping.yaml'
cloudformation_multiple_trustzones_same_type_mapping = \
    path + '/mapping/cloudformation_multiple_trustzones_same_type_mapping.yaml'
cloudformation_old_default_mapping = path + '/mapping/cloudformation_old_default_mapping.yaml'
cloudformation_new_default_mapping = path + '/mapping/cloudformation_new_default_mapping.yaml'
cloudformation_mapping_valid_without_trustzone_type = path + '/mapping/cloudformation_mapping_valid_without_trustzone_type.yaml'

# cft
cloudformation_for_mappings_tests_json = path + '/cft/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = path + '/cft/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json = path + '/cft/cloudformation_for_security_group_tests_2.json'
cloudformation_gz = path + '/cft/cloudformation.gz'
cloudformation_invalid_size = path + '/cft/cloudformation-invalid-size.json'
cloudformation_component_without_parent = path + '/cft/cloudformation_component_without_parent.json'
cloudformation_skipped_component_without_parent = path + '/cft/cloudformation_component_without_parent_skipped.json'
cloudformation_unknown_resource = path + '/cft/cloudformation_unknown_resource.json'
cloudformation_all_functions = path + '/cft/cloudformation_all_functions.json'
cloudformation_single_file = path + '/cft/cloudformation_single_file.json'
cloudformation_networks_file = path + '/cft/cloudformation_networks_file.json'
cloudformation_resources_file = path + '/cft/cloudformation_resources_file.json'
cloudformation_resources_invalid = path + '/cft/cloudformation_resources_invalid.json'
cloudformation_react_cors_spa_stack = path + '/cft/cloudformation_react_cors_spa_stack.yaml'
cloudformation_test = path + '/cft/cloudformation_test.yaml'
multiple_stack_plus_s3_ec2 = path + '/cft/multiple_stack_plus_s3_ec2.yaml'
standalone_securitygroupegress_configuration = path + '/cft/standalone_securitygroupegress_configuration.yaml'
standalone_securitygroupingress_configuration = path + '/cft/standalone_securitygroupingress_configuration.yaml'
cloudformation_minimal_content = path + '/cft/cloudformation_minimal_content.json'
cloudformation_orphan_component = path + '/cft/cloudformation_orphan_component.json'
altsource_components_json = path + '/cft/altsource_components.json'
altsource_components_otm_expected = path + '/otm/expected_altsource_components.otm'
cloudformation_with_ref_function_and_default_property_json = path + '/cft/cloudformation_with_ref_and_default.json'
cloudformation_with_ref_function_and_without_default_property_json = \
    path + '/cft/cloudformation_with_ref_and_without_default.json'
cloudformation_with_ref_function_and_default_property_yaml = path + '/cft/cloudformation_with_ref_and_default.yaml'
cloudformation_with_ref_function_and_without_parameters = path + \
                                                       '/cft/cloudformation_with_ref_and_without_parameters.json'
cloudformation_components_from_same_resource = path + '/cft/cloudformation_components_from_same_resource.json'
cloudformation_components_with_trustzones_of_same_type = \
    path + '/cft/cloudformation_components_with_trustzones_of_same_type.json'

# otm
otm_expected_result = path + '/otm/otm_expected_result.otm'
expected_orphan_component_is_not_mapped = path + '/otm/expected_orphan_component_is_not_mapped.otm'
otm_with_only_default_trustzone_expected_result = path + '/otm/otm_with_only_default_trustzone_expected_result.otm'
minimal_otm_expected_result = path + '/otm/minimal_otm_expected_result.otm'
cft_components_with_trustzones_of_same_type_otm = f'{path}/otm/cft_components_with_trustzones_of_same_type.otm'
cloudformation_minimal_content_otm = f'{path}/otm/cloudformation_minimal_content.otm'

