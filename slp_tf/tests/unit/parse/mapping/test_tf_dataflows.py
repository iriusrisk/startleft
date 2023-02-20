import pytest
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from sl_util.sl_util.file_utils import get_data

TF_MAPPING_FILE = test_resource_paths.terraform_iriusrisk_tf_aws_mapping
TF_MAPPING_FILE_V180 = test_resource_paths.terraform_iriusrisk_tf_aws_mapping_v180
SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformDataflows:

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_to_lambda_function(self, mapping_file):
        # GIVEN a valid TF file with an aws_lambda_function resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_lambda_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'dataflow to Lambda function in basic_dynamodb_event'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'basic_dynamodb_table', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'basic_dynamodb_table', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'basic_lambda', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'basic_lambda', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_to_lambda_function_on_failure(self, mapping_file):
        # GIVEN a valid TF file with an aws_lambda_function on failure resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_lambda_on_failure_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'dataflow from Lambda function on Failure basic_dynamodb_event'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'basic_lambda', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'basic_lambda', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'failure_queue', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'failure_queue', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_s3(self, mapping_file):
        # GIVEN a valid TF file with an aws_s3_bucket resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_s3_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'S3 dataflow from bucket_deprecated'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'bucket_deprecated', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'bucket_deprecated', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'log_bucket_deprecated', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'log_bucket_deprecated', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_s3_bucket_logging(self, mapping_file):
        # GIVEN a valid TF file with an aws_s3_bucket_logging resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_s3_bucket_logging_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'S3 dataflow from aws_s3_bucket_logging'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'bucket', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'bucket', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'log_bucket', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'log_bucket', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_api_gateway_one_source(self, mapping_file):
        # GIVEN a valid TF file with an aws_api_gateway_authorizer resource
        # AND a single api resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_api_gateway_authorizer_one_source_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'API gateway data flow from aws_api_gateway_authorizer'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'api_authorizer', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'api_authorizer', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'user_pool', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'user_pool', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_api_gateway_multiple_sources(self, mapping_file):
        # GIVEN a valid TF file with an aws_api_gateway_authorizer resource
        # AND multiple api resource
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_api_gateway_authorizer_multiple_sources_dataflow)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'API gateway data flow from aws_api_gateway_authorizer'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'api-gateway (grouped)', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'api-gateway (grouped)', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'user_pool', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'user_pool', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_outbound(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SG -> B
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_outbound)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'VPCssm -> VPCssmSecurityGroup'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))
        destination_component = list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_outbound_two_subnets(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SG -> B
        # AND 2 subnets
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_outbound_two_subnets)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 2

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'VPCssm -> VPCssmSecurityGroup'

        # AND both dataflows have the same name
        assert otm.dataflows[0].name == otm.dataflows[1].name

        # AND both dataflows have the same destination
        assert otm.dataflows[0].destination_node == otm.dataflows[1].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_inbound(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SG -> B
        # AND a CustomVPC
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_inbound)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'VPCssmSecurityGroup -> VPCssm'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'CustomVPC', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'CustomVPC', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_inbound_two_subnets(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SG -> B
        # AND 2 subnets
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_inbound_two_subnets)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 2

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'VPCssmSecurityGroup -> VPCssm'

        # AND both dataflows have the same name
        assert otm.dataflows[0].name == otm.dataflows[1].name

        # AND both dataflows have the same source node
        assert otm.dataflows[0].source_node == otm.dataflows[1].source_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_inbound_with_generic_component(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SG -> B
        # AND without a CustomVPC
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_inbound_with_generic_client)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 2

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'VPCssmSecurityGroup -> VPCssm'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == '10.0.0.0/16', otm.components))
        source_component = list(filter(lambda obj: obj.name == '10.0.0.0/16', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type2_outbound(self, mapping_file):
        # GIVEN a valid TF file with security groups type 2: A -> SGA -> SGB -> B
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type2_outbound)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'ServiceLB -> Service'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'Service', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'Service', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type2_outbound_two_subnets(self, mapping_file):
        # GIVEN a valid TF file with security groups type 2: A -> SGA -> SGB -> B and two subnets both in Service
        # AND in ServiceLB
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type2_outbound_two_subnets)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 4
        assert len(otm.dataflows) == 4

        # AND there are 4 dataflows with the same name
        assert len(list(filter(lambda obj: obj.name == 'ServiceLB -> Service', otm.dataflows))) == 4

        # AND there are two dataflows which source has 'privatesubnet1'
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        service_components = list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        private_subnet_1_dataflows = list(filter(lambda obj: obj.source_node == service_components[0].id,
                                                 otm.dataflows))
        assert len(private_subnet_1_dataflows) == 2

        # AND these two dataflows have the same source but distinct destination
        assert private_subnet_1_dataflows[0].source_node == private_subnet_1_dataflows[1].source_node
        assert private_subnet_1_dataflows[0].destination_node != private_subnet_1_dataflows[1].destination_node

        # AND there are two dataflows which source has 'privatesubnet2'
        private_subnet_2_dataflows = list(filter(lambda obj: obj.source_node == service_components[1].id,
                                                 otm.dataflows))
        assert len(private_subnet_1_dataflows) == 2

        # AND these two dataflows have the same source but distinct destination
        assert private_subnet_2_dataflows[0].source_node == private_subnet_2_dataflows[1].source_node
        assert private_subnet_2_dataflows[0].destination_node != private_subnet_2_dataflows[1].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type2_inbound(self, mapping_file):
        # GIVEN a valid TF file with security groups type 2: A -> SGA -> SGB -> B
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type2_inbound)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 1
        assert len(otm.dataflows) == 1

        # AND the dataflow name is correct
        assert otm.dataflows[0].name == 'Canary -> ServiceLB'

        # AND the source code is correct
        assert list(filter(lambda obj: obj.name == 'Canary', otm.components))
        source_component = list(filter(lambda obj: obj.name == 'Canary', otm.components))
        assert source_component[0].id == otm.dataflows[0].source_node

        # AND the destination node is correct
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        destination_component = list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        assert destination_component[0].id == otm.dataflows[0].destination_node

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(TF_MAPPING_FILE), id="with actual mapping file"),
        pytest.param(get_data(TF_MAPPING_FILE_V180), id="with backwards mapping_file")])
    def test_tf_dataflow_security_group_type1_and_type2_mixed(self, mapping_file):
        # GIVEN a valid TF file with security groups type 1: A -> SGA -> B and type 2: A -> SGA -> SGB -> B
        # AND a valid TF mapping file
        tf_file = get_data(test_resource_paths.terraform_security_groups_type1_and_type2_mixed)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN the number of dataflows is 2
        assert len(otm.dataflows) == 2

        # AND the dataflow names are correct
        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service', otm.dataflows))
        assert list(filter(lambda obj: obj.name == 'Service -> OutboundSecurityGroup', otm.dataflows))

        # AND the source codes are correct
        type1_dataflow = list(filter(lambda obj: obj.name == 'Service -> OutboundSecurityGroup', otm.dataflows))
        assert list(filter(lambda obj: obj.name == 'Service', otm.components))
        type1_component = list(filter(lambda obj: obj.name == 'Service', otm.components))
        assert type1_component[0].id == type1_dataflow[0].source_node

        type2_dataflow = list(filter(lambda obj: obj.name == 'ServiceLB -> Service', otm.dataflows))
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        type2_component = list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        assert type2_component[0].id == type2_dataflow[0].source_node

        # AND the destination nodes are correct
        assert list(filter(lambda obj: obj.name == '255.255.255.255/32', otm.components))
        type1_destination_component = list(filter(lambda obj: obj.name == '255.255.255.255/32', otm.components))
        assert type1_destination_component[0].id == type1_dataflow[0].destination_node
        assert type1_component[0].id == type2_dataflow[0].destination_node


