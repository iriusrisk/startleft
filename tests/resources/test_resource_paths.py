import os

path = os.path.dirname(__file__)

# GENERIC
example_json = path + '/example.json'
example_yaml = path + '/example.yaml'
invalid_yaml = path + '/invalid-yaml.yaml'
invalid_tf = path + '/invalid-tf.tf'
example_gzip = path + '/example.gz'
empty_mapping_file = path + "/empty_mapping_file.yaml"

# OTM
otm_file_example = path + '/otm/otm_file_example.otm'
otm_yaml_file_example = path + '/otm/otm_file_example_yaml.otm'
otm_empty_file_example = path + '/otm/otm_empty_file_example.otm'

# CLOUDFORMATION
cloudformation_for_mappings_tests_json = path + '/cloudformation/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = path + '/cloudformation/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json = path + '/cloudformation/cloudformation_for_security_group_tests_2.json'
cloudformation_for_security_groups_mapping = path + '/cloudformation/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_gz = path + '/cloudformation/cloudformation.gz'
cloudformation_invalid_size = path + '/cloudformation/cloudformation-invalid-size.json'
cloudformation_malformed_mapping_wrong_id = path + '/cloudformation/cloudformation_malformed_mapping_wrong_id.yaml'
cloudformation_component_without_parent = path + '/cloudformation/cloudformation_component_without_parent.json'
cloudformation_skipped_component_without_parent = path + '/cloudformation/cloudformation_component_without_parent_skipped.json'
cloudformation_unknown_resource = path + '/cloudformation/cloudformation_unknown_resource.json'
cloudformation_all_functions = path + '/cloudformation/cloudformation_all_functions.json'
# mapping
default_cloudformation_mapping = path + '/cloudformation/cloudformation_mapping.yaml'
cloudformation_mapping_component_without_parent = path + '/cloudformation/cloudformation_mapping_component_without_parent.yaml'
cloudformation_mapping_all_functions = path + '/cloudformation/cloudformation_mapping_all_functions.yaml'
# expected otm results
cloudformation_for_mappings_tests_json_otm_expected = path + '/cloudformation/cloudformation_for_mappings_tests.otm'

# TERRAFORM
terraform_for_mappings_tests_json = path + '/terraform/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = path + '/terraform/aws_simple_components.tf'
terraform_aws_multiple_components = path + '/terraform/aws_multiple_components.tf'
terraform_aws_singleton_components = path + '/terraform/aws_singleton_components.tf'
terraform_aws_altsource_components = path + '/terraform/aws_altsource_components.tf'
terraform_aws_security_groups_components = path + '/terraform/aws_security_groups_components.tf'
terraform_aws_dataflows = path + '/terraform/aws_dataflows.tf'
terraform_aws_parent_children_components = path + '/terraform/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = path + '/terraform/aws_singleton_components_unix_line_breaks.tf'
terraform_component_without_parent = path + '/terraform/aws_component_without_parent.tf'
terraform_skipped_component_without_parent = path + '/terraform/aws_component_without_parent_skipped.tf'
terraform_unknown_resource = path + '/terraform/terraform_unknown_resource.tf'
terraform_unknown_module = path + '/terraform/terraform_unknown_module.tf'
terraform_no_resources = path + '/terraform/no_resources.tf'
terraform_gz = path + '/terraform/terraform.gz'
terraform_specific_functions = path + '/terraform/terraform_specific_functions.tf'
terraform_modules = path + '/terraform/terraform_modules_sample.tf'
terraform_extra_modules_sample = path + '/terraform/terraform_extra_modules_sample.tf'
# mapping
default_terraform_mapping = path + '/terraform/default-terraform-mapping.yaml'
default_terraform_aws_mapping = path + '/terraform/aws_terraform_mapping.yaml'
terraform_mapping_aws_component_without_parent = path + '/terraform/terraform_mapping_component_without_parent.yaml'
terraform_malformed_mapping_wrong_id = path + '/terraform/terraform-malformed-mapping-wrong-id.yaml'
terraform_mapping_specific_functions = path + '/terraform/terraform_mapping_specific_functions.yaml'
terraform_mapping_modules = path + '/terraform/terraform_mapping_modules.yaml'
terraform_mapping_extra_modules = path + '/terraform/terraform_mapping_extra_modules.yaml'
# expected otm results
terraform_aws_simple_components_otm_expected = path + '/terraform/aws_simple_components.otm'

# VISIO
visio_aws_with_tz_and_vpc = path + '/visio/aws-with-tz-and-vpc.vsdx'
visio_aws_shapes = path + '/visio/aws-shapes.vsdx'
visio_aws_stencils = path + '/visio/aws-stencils.vsdx'
visio_generic_shapes = path + '/visio/generic-shapes.vsdx'
visio_self_pointing_connectors = path + '/visio/self-pointing-connectors.vsdx'
visio_extraneous_elements = path + '/visio/extraneous-elements.vsdx'
visio_boundaries = path + '/visio/boundaries.vsdx'
visio_simple_boundary_tzs = path + '/visio/simple-boundary-tzs.vsdx'
visio_boundary_tz_and_default_tz = path + '/visio/boundary-tz-and-default-tz.vsdx'
visio_overlapped_boundary_tzs = path + '/visio/overlapped-boundary-tzs.vsdx'
visio_multiple_pages_diagram = path + '/visio/multiple-pages-diagram.vsdx'
visio_boundary_and_component_tzs = path + '/visio/boundary-and-component-tzs.vsdx'
visio_nested_tzs = path + '/visio/nested-tzs.vsdx'
visio_simple_components = path + '/visio/simple-components.vsdx'
visio_orphan_dataflows = path + '/visio/visio-orphan-dataflows.vsdx'
visio_invalid_file_size = path + '/visio/invalid-file-size.vsdx'
visio_invalid_file_type = path + '/visio/invalid-file-type.pdf'
# mapping
default_visio_mapping = path + '/visio/aws-visio-mapping.yaml'
custom_vpc_mapping = path + '/visio/custom-vpc-mapping.yaml'
# expected otm results
visio_aws_shapes_otm_expected = path + '/visio/aws-shapes.otm'
visio_aws_with_tz_and_vpc_otm_expected = path + '/visio/aws-with-tz-and-vpc.otm'
visio_orphan_dataflows_otm_expected = path + '/visio/visio-orphan-dataflows.otm'

# MTMT
model_mtmt_source_file = path + '/mtmt/test_model.tm7'
mtmt_mapping_file = path + '/mtmt/mtmt-mapping.yaml'
