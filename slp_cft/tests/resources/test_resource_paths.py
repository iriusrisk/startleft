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
multiple_stack_plus_s3_ec2 = path + '/cft/multiple_stack_plus_s3_ec2.yaml'
standalone_securitygroupegress_configuration = path + '/cft/standalone_securitygroupegress_configuration.yaml'
standalone_securitygroupingress_configuration = path + '/cft/standalone_securitygroupingress_configuration.yaml'
cloudformation_component_with_unknown_parent = path + '/cft/cloudformation_component_with_unknown_parent.json'

# otm
otm_expected_result = path + '/otm/otm_expected_result.otm'
expected_set_default_trustzone_as_parent_when_parent_not_exists = path + '/otm/expected_set_default_trustzone_as_parent_when_parent_not_exists.otm'