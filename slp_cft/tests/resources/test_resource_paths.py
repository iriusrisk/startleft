import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'

# mapping
default_cloudformation_mapping = path + '/mapping/cloudformation_mapping.yaml'
cloudformation_mapping_component_without_parent = path + '/mapping/cloudformation_mapping_component_without_parent.yaml'
cloudformation_mapping_all_functions = path + '/mapping/cloudformation_mapping_all_functions.yaml'
cloudformation_for_security_groups_mapping = path + '/mapping/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_malformed_mapping_wrong_id = path + '/mapping/cloudformation_malformed_mapping_wrong_id.yaml'

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
