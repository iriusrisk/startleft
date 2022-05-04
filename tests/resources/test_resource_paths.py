import os

from tests.diagram.test_visio_diagram_to_otm import AWS_WITH_TRUSTZONES_AND_VPC_FILENAME

cloudformation_for_mappings_tests_json = os.path.dirname(__file__) + '/cloudformation_for_mappings_tests.json'
cloudformation_for_security_group_tests_json = os.path.dirname(__file__)+'/cloudformation_for_security_group_tests.json'
cloudformation_for_security_group_tests_2_json =\
    os.path.dirname(__file__)+'/cloudformation_for_security_group_tests_2.json'
cloudformation_for_security_groups_mapping = os.path.dirname(__file__)\
                                             + '/cloudformation_for_security_group_tests_mapping_definitions.yaml'
default_mapping = os.path.dirname(__file__)+'/../../startleft/config/default-cloudformation-mapping.yaml'
default_terraform_aws_mapping = os.path.dirname(__file__)+'/../../startleft/config/default-terraform-mapping.yaml'
example_json = os.path.dirname(__file__) + '/example.json'
example_yaml = os.path.dirname(__file__) + '/example.yaml'
terraform_for_mappings_tests_json = os.path.dirname(__file__) + '/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = os.path.dirname(__file__) + '/terraform/aws_simple_components.tf'
terraform_aws_singleton_components = os.path.dirname(__file__) + '/terraform/aws_singleton_components.tf'
invalid_yaml = os.path.dirname(__file__) + '/invalid-yaml.yaml'

otm_file_example = os.path.dirname(__file__) + '/otm_file_example.otm'

aws_with_trustzones_and_vpc_input_path = os.path.dirname(__file__) + '/visio/' + AWS_WITH_TRUSTZONES_AND_VPC_FILENAME + '.vsdx'
