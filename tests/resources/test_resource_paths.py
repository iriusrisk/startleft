import os

path = os.path.dirname(__file__)

# GENERIC
example_json = path + '/example.json'
example_yaml = path + '/example.yaml'
invalid_yaml = path + '/invalid-yaml.yaml'

# OTM
otm_file_example = path + '/otm/otm_file_example.otm'

# CLOUDFORMATION
cloudformation_for_mappings_tests_json = path + '/cloudformation/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = path + '/cloudformation/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json = path + '/cloudformation/cloudformation_for_security_group_tests_2.json'
cloudformation_for_security_groups_mapping = path + '/cloudformation/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_malformed_mapping_wrong_id = path + '/cloudformation/cloudformation_malformed_mapping_wrong_id.yaml'
# mapping
default_cloudformation_mapping = path + '/../../startleft/resources/defaultmappings/default-cloudformation-mapping.yaml'

# TERRAFORM
terraform_for_mappings_tests_json = path + '/terraform/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = path + '/terraform/aws_simple_components.tf'
terraform_aws_singleton_components = path + '/terraform/aws_singleton_components.tf'
terraform_aws_parent_children_components = path + '/terraform/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = path + '/terraform/aws_singleton_components_unix_line_breaks.tf'
terraform_aws_singleton_components_dos_line_breaks = path + '/terraform/aws_singleton_components_dos_line_breaks.tf'
terraform_aws_singleton_components_classic_macos_line_breaks = path + '/terraform/aws_singleton_components_classic_macos_line_breaks.tf'

# mapping
default_terraform_aws_mapping = path + '/../../startleft/resources/defaultmappings/default-terraform-mapping.yaml'

# VISIO
visio_aws_with_tz_and_vpc = path + '/visio/aws-with-tz-and-vpc.vsdx'
visio_aws_shapes = path + '/visio/aws-shapes.vsdx'
visio_generic_shapes = path + '/visio/generic-shapes.vsdx'
visio_self_pointing_connectors = path + '/visio/self-pointing-connectors.vsdx'
visio_extraneous_elements = path + '/visio/extraneous-elements.vsdx'
# mapping
default_visio_mapping = path + '/../../startleft/resources/defaultmappings/default-visio-mapping.yaml'
custom_vpc_mapping = path + '/visio/custom-vpc-mapping.yaml'
