import os

path = os.path.dirname(__file__)

# GENERIC
example_json = f'{path}/example.json'
example_yaml = f'{path}/example.yaml'
example_template = f'{path}/example.template'
invalid_yaml = f'{path}/invalid-yaml.yaml'
invalid_tf = f'{path}/invalid-tf.tf'
example_gzip = f'{path}/example.gz'
empty_mapping_file = path + "/empty_mapping_file.yaml"

# OTM
otm_file_example = f'{path}/otm/otm_file_example.otm'
otm_yaml_file_example = f'{path}/otm/otm_file_example_yaml.otm'
otm_empty_file_terraform_example = f'{path}/otm/otm_empty_file_terraform_example.otm'
otm_empty_file_cloudformation_example = f'{path}/otm/otm_empty_file_cloudformation_example.otm'

# CLOUDFORMATION
cloudformation_for_mappings_tests_json = f'{path}/cloudformation/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = f'{path}/cloudformation/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json = f'{path}/cloudformation/cloudformation_for_security_group_tests_2.json'
cloudformation_for_security_groups_mapping = f'{path}/cloudformation/cloudformation_for_security_group_tests_mapping_definitions.yaml'
cloudformation_gz = f'{path}/cloudformation/cloudformation.gz'
cloudformation_empty_file = f'{path}/cloudformation/cloudformation_empty_file.json'
cloudformation_invalid_size = f'{path}/cloudformation/cloudformation-invalid-size.json'
cloudformation_malformed_mapping_wrong_id = f'{path}/cloudformation/cloudformation_malformed_mapping_wrong_id.yaml'
cloudformation_component_without_parent = f'{path}/cloudformation/cloudformation_component_without_parent.json'
cloudformation_skipped_component_without_parent = f'{path}/cloudformation/cloudformation_component_without_parent_skipped.json'
cloudformation_unknown_resource = f'{path}/cloudformation/cloudformation_unknown_resource.json'
cloudformation_all_functions = f'{path}/cloudformation/cloudformation_all_functions.json'
cloudformation_multiple_files_networks = f'{path}/cloudformation/cloudformation_multiple_files_networks.json'
cloudformation_multiple_files_resources = f'{path}/cloudformation/cloudformation_multiple_files_resources.json'
cloudformation_ref_full_syntax = f'{path}/cloudformation/cloudformation_ref_full_syntax.yaml'
cloudformation_ref_short_syntax = f'{path}/cloudformation/cloudformation_ref_short_syntax.yaml'
# mapping
default_cloudformation_mapping = f'{path}/cloudformation/cloudformation_mapping.yaml'
old_cloudformation_default_mapping = f'{path}/cloudformation/old_cloudformation_default_mapping.yaml'
cloudformation_mapping_component_without_parent = f'{path}/cloudformation/cloudformation_mapping_component_without_parent.yaml'
cloudformation_mapping_all_functions = f'{path}/cloudformation/cloudformation_mapping_all_functions.yaml'
cloudformation_mapping_no_dataflows = f'{path}/cloudformation/cloudformation_mapping_no_dataflows.yaml'
cloudformation_mapping_trustzone_no_id = f'{path}/cloudformation/cloudformation_mapping_trustzone_no_id.yaml'
cloudformation_custom_mapping_file = f'{path}/cloudformation/cloudformation_custom_mapping_file.yaml'
cloudformation_wrong_mapping_file = f'{path}/cloudformation/cloudformation_wrong_mapping_file.yaml'

# expected otm results
cloudformation_for_mappings_tests_json_otm_expected = f'{path}/cloudformation/cloudformation_for_mappings_tests.otm'

# TERRAFORM
terraform_for_mappings_tests_json = f'{path}/terraform/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = f'{path}/terraform/aws_simple_components.tf'
terraform_aws_multiple_components = f'{path}/terraform/aws_multiple_components.tf'
terraform_aws_singleton_components = f'{path}/terraform/aws_singleton_components.tf'
terraform_aws_altsource_components = f'{path}/terraform/aws_altsource_components.tf'
terraform_aws_security_groups_components = f'{path}/terraform/aws_security_groups_components.tf'
terraform_aws_dataflows = f'{path}/terraform/aws_dataflows.tf'
terraform_aws_parent_children_components = f'{path}/terraform/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = f'{path}/terraform/aws_singleton_components_unix_line_breaks.tf'
terraform_component_without_parent = f'{path}/terraform/aws_component_without_parent.tf'
terraform_skipped_component_without_parent = f'{path}/terraform/aws_component_without_parent_skipped.tf'
terraform_unknown_resource = f'{path}/terraform/terraform_unknown_resource.tf'
terraform_unknown_module = f'{path}/terraform/terraform_unknown_module.tf'
terraform_no_resources = f'{path}/terraform/no_resources.tf'
terraform_gz = f'{path}/terraform/terraform.gz'
terraform_specific_functions = f'{path}/terraform/terraform_specific_functions.tf'
terraform_modules = f'{path}/terraform/terraform_modules_sample.tf'
terraform_extra_modules_sample = f'{path}/terraform/terraform_extra_modules_sample.tf'
terraform_multiple_files_one = f'{path}/terraform/aws_simple_components.tf'
terraform_multiple_files_two = f'{path}/terraform/aws_dataflows.tf'
# mapping
terraform_iriusrisk_tf_aws_mapping = f'{path}/terraform/iriusrisk-tf-aws-mapping.yaml'
terraform_mapping_aws_component_without_parent = f'{path}/terraform/terraform_mapping_component_without_parent.yaml'
terraform_malformed_mapping_wrong_id = f'{path}/terraform/terraform-malformed-mapping-wrong-id.yaml'
terraform_mapping_specific_functions = f'{path}/terraform/terraform_mapping_specific_functions.yaml'
terraform_mapping_modules = f'{path}/terraform/terraform_mapping_modules.yaml'
terraform_mapping_extra_modules = f'{path}/terraform/terraform_mapping_extra_modules.yaml'
# expected otm results
terraform_aws_simple_components_otm_expected = f'{path}/terraform/aws_simple_components.otm'

# TERRAFORM PLAN
terraform_plan_official = f'{path}/tfplan/official-tfplan.json'
terraform_graph_official = f'{path}/tfplan/official-tfgraph.gv'
# mapping
terraform_plan_default_mapping_file = f'{path}/tfplan/iriusrisk-tfplan-aws-mapping.yaml'
terraform_plan_custom_mapping_file = f'{path}/tfplan/iriusrisk-tfplan-custom-mapping.yaml'


# VISIO
visio_aws_vsdx_folder = f'{path}/visio/'
visio_aws_with_tz_and_vpc = f'{path}/visio/aws-with-tz-and-vpc.vsdx'
visio_aws_shapes = f'{path}/visio/aws-shapes.vsdx'
visio_aws_stencils = f'{path}/visio/aws-stencils.vsdx'
visio_generic_shapes = f'{path}/visio/generic-shapes.vsdx'
visio_self_pointing_connectors = f'{path}/visio/self-pointing-connectors.vsdx'
visio_extraneous_elements = f'{path}/visio/extraneous-elements.vsdx'
visio_boundaries = f'{path}/visio/boundaries.vsdx'
visio_simple_boundary_tzs = f'{path}/visio/simple-boundary-tzs.vsdx'
visio_boundary_tz_and_default_tz = f'{path}/visio/boundary-tz-and-default-tz.vsdx'
visio_overlapped_boundary_tzs = f'{path}/visio/overlapped-boundary-tzs.vsdx'
visio_multiple_pages_diagram = f'{path}/visio/multiple-pages-diagram.vsdx'
visio_boundary_and_component_tzs = f'{path}/visio/boundary-and-component-tzs.vsdx'
visio_nested_tzs = f'{path}/visio/nested-tzs.vsdx'
visio_simple_components = f'{path}/visio/simple-components.vsdx'
visio_orphan_dataflows = f'{path}/visio/visio-orphan-dataflows.vsdx'
visio_invalid_file_size = f'{path}/visio/invalid-file-size.vsdx'
visio_invalid_file_type = f'{path}/visio/invalid-file-type.pdf'
visio_modified_single_connectors = f'{path}/visio/modified-single-connectors.vsdx'
visio_bidirectional_connectors = f'{path}/visio/bidirectional-connectors.vsdx'
# mapping
default_visio_mapping = f'{path}/visio/aws-visio-mapping.yaml'
custom_vpc_mapping = f'{path}/visio/custom-vpc-mapping.yaml'

# legacy mapping
default_visio_mapping_legacy = f'{path}/visio/legacy/aws-visio-mapping.yaml'
custom_vpc_mapping_legacy = f'{path}/visio/legacy/custom-vpc-mapping.yaml'

# expected otm results
visio_aws_shapes_otm_expected = f'{path}/visio/aws-shapes.otm'
visio_aws_with_tz_and_vpc_otm_expected = f'{path}/visio/aws-with-tz-and-vpc.otm'
visio_orphan_dataflows_otm_expected = f'{path}/visio/visio-orphan-dataflows.otm'
visio_create_otm_ok_only_default_mapping = f'{path}/visio/visio_create_otm_ok_only_default_mapping.otm'
MTMT_multiple_trustzones_same_type_ID = f'{path}/otm/MTMT_multiple_trustzones_same_type_ID.otm'
MTMT_multiple_trustzones_same_type_TYPE = f'{path}/otm/MTMT_multiple_trustzones_same_type_TYPE.otm'

# LUCID
lucid_aws_vsdx_folder = f'{path}/lucid/'
lucid_aws_with_tz = f'{path}/lucid/lucid-aws-with-tz.vsdx'
lucid_aws_with_tz_and_vpc = f'{path}/lucid/lucid-aws-with-tz-and-vpc.vsdx'
lucid_summary_expected_summary = f'{path}/lucid/summary-expected-summary.csv'
# mapping
default_lucid_mapping = f'{path}/lucid/default-lucid-mapping.yaml'
lucid_aws_with_tz_mapping = f'{path}/lucid/lucid-aws-with-tz.yaml'
lucid_aws_with_tz_and_vpc_mapping = f'{path}/lucid/lucid-aws-with-tz-and-vpc.yaml'
# expected otm results
lucid_aws_with_tz_default_otm = f'{path}/lucid/lucid-aws-with-tz-default.otm'
lucid_aws_with_tz_otm = f'{path}/lucid/lucid-aws-with-tz.otm'
lucid_aws_with_tz_and_vpc_otm = f'{path}/lucid/lucid-aws-with-tz-and-vpc.otm'

# MTMT
mtmt_mapping_file_valid = f'{path}/mtmt/mapping_example.yaml'
mtmt_mapping_file_invalid = f'{path}/mtmt/mapping_example_invalid.yaml'

# DRAWIO
drawio_multi_page = f'{path}/drawio/drawio-multi-page.drawio'
default_drawio_mapping = f'{path}/drawio/drawio_mapping.yaml'
drawio_minimal_xml = f'{path}/drawio/aws_minimal.drawio.xml'
drawio_minimal_drawio = f'{path}/drawio/aws_minimal.drawio'
lean_ix_drawio = f'{path}/drawio/lean_ix.drawio.xml'
custom_drawio_mapping = f'{path}/drawio/custom_drawio_mapping.yaml'
invalid_extension_mtmt_file = f'{path}/drawio/invalid-extension-mtmt-mobile-api.tm7'
