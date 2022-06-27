import os

path = os.path.dirname(__file__)

# GENERIC
example_json = path + '/example.json'
example_yaml = path + '/example.yaml'
invalid_yaml = path + '/invalid-yaml.yaml'
example_gzip = path + '/example.gz'

# OTM
otm_file_example = path + '/otm/otm_file_example.otm'

# CLOUDFORMATION
cloudformation_for_mappings_tests_json = path + '/cloudformation/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = path + '/cloudformation/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json = path + '/cloudformation/cloudformation_for_security_group_tests_2.json'
cloudformation_for_security_groups_mapping = path + '/cloudformation/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_malformed_mapping_wrong_id = path + '/cloudformation/cloudformation_malformed_mapping_wrong_id.yaml'
cloudformation_component_without_parent = path + '/cloudformation/cloudformation_component_without_parent.json'
cloudformation_skipped_component_without_parent = path + '/cloudformation/cloudformation_component_without_parent_skipped.json'
# mapping
default_cloudformation_mapping = path + '/cloudformation/cloudformation_mapping.yaml'
cloudformation_mapping_component_without_parent = path + '/cloudformation/cloudformation_mapping_component_without_parent.yaml'

# TERRAFORM
terraform_for_mappings_tests_json = path + '/terraform/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = path + '/terraform/aws_simple_components.tf'
terraform_aws_singleton_components = path + '/terraform/aws_singleton_components.tf'
terraform_aws_parent_children_components = path + '/terraform/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = path + '/terraform/aws_singleton_components_unix_line_breaks.tf'
terraform_component_without_parent = path + '/terraform/aws_component_without_parent.tf'
terraform_skipped_component_without_parent = path + '/terraform/aws_component_without_parent_skipped.tf'

# mapping
default_terraform_mapping = path + '/terraform/default-terraform-mapping.yaml'
default_terraform_aws_mapping = path + '/terraform/aws_terraform_mapping.yaml'
terraform_mapping_aws_component_without_parent = path + '/terraform/terraform_mapping_component_without_parent.yaml'

# VISIO
visio_aws_with_tz_and_vpc = path + '/visio/aws-with-tz-and-vpc.vsdx'
visio_aws_shapes = path + '/visio/aws-shapes.vsdx'
visio_generic_shapes = path + '/visio/generic-shapes.vsdx'
visio_self_pointing_connectors = path + '/visio/self-pointing-connectors.vsdx'
visio_extraneous_elements = path + '/visio/extraneous-elements.vsdx'
# mapping
default_visio_mapping = path + '/visio/aws-visio-mapping.yaml'
custom_vpc_mapping = path + '/visio/custom-vpc-mapping.yaml'
