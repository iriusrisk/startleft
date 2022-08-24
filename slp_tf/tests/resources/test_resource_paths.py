import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'
invalid_tf = path + '/generic/invalid-tf.tf'

# tf
terraform_for_mappings_tests_json = path + '/tf/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = path + '/tf/aws_simple_components.tf'
terraform_aws_multiple_components = path + '/tf/aws_multiple_components.tf'
terraform_aws_singleton_components = path + '/tf/aws_singleton_components.tf'
terraform_aws_altsource_components = path + '/tf/aws_altsource_components.tf'
terraform_aws_security_groups_components = path + '/tf/aws_security_groups_components.tf'
terraform_aws_dataflows = path + '/tf/aws_dataflows.tf'
terraform_aws_parent_children_components = path + '/tf/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = path + '/tf/aws_singleton_components_unix_line_breaks.tf'
terraform_component_without_parent = path + '/tf/aws_component_without_parent.tf'
terraform_skipped_component_without_parent = path + '/tf/aws_component_without_parent_skipped.tf'
terraform_unknown_resource = path + '/tf/terraform_unknown_resource.tf'
terraform_unknown_module = path + '/tf/terraform_unknown_module.tf'
terraform_no_resources = path + '/tf/no_resources.tf'
terraform_gz = path + '/tf/terraform.gz'
terraform_specific_functions = path + '/tf/terraform_specific_functions.tf'
terraform_modules = path + '/tf/terraform_modules_sample.tf'
terraform_extra_modules_sample = path + '/tf/terraform_extra_modules_sample.tf'

# mapping
default_terraform_mapping = path + '/mapping/default-terraform-mapping.yaml'
default_terraform_aws_mapping = path + '/mapping/aws_terraform_mapping.yaml'
terraform_mapping_aws_component_without_parent = path + '/mapping/terraform_mapping_component_without_parent.yaml'
terraform_malformed_mapping_wrong_id = path + '/mapping/terraform-malformed-mapping-wrong-id.yaml'
terraform_mapping_specific_functions = path + '/mapping/terraform_mapping_specific_functions.yaml'
terraform_mapping_modules = path + '/mapping/terraform_mapping_modules.yaml'
terraform_mapping_extra_modules = path + '/mapping/terraform_mapping_extra_modules.yaml'
