import pytest

from sl_util.sl_util.file_utils import get_data, get_byte_data
from slp_base.slp_base.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_base.tests.util import otm as utils
from slp_base.tests.util.otm import validate_and_diff_otm
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import expected_orphan_component_is_not_mapped
from slp_tf.tests.utility import excluded_regex

PUBLIC_CLOUD_TZ_ID = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
INTERNET_TZ_ID = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
DEFAULT_TRUSTZONE_ID = "b61d6911-338d-46a8-9f39-8dcd24abfe91"
SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_TF_FILE = test_resource_paths.terraform_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.default_terraform_aws_mapping


def assert_otm_trustzone(otm, position, id, name):
    assert otm.trustzones[position].id == id
    assert otm.trustzones[position].name == name


def assert_otm_component(otm, position, type, name, parent, tags):
    assert otm.components[position].type == type
    assert otm.components[position].name == name

    if parent is not None:
        assert otm.components[position].parent == parent

    for c_tag in tags:
        assert c_tag in otm.components[position].tags


def assert_otm_dataflow(otm, position, source_node, destination_node, name):
    assert otm.dataflows[position].source_node == source_node
    assert otm.dataflows[position].destination_node == destination_node
    assert otm.dataflows[position].name == name


class TestTerraformProcessor:

    def test_orphan_component_is_not_mapped(self):
        # GIVEN a valid TF file with a resource (VPCssm) whose parents do (private VPCs) not exist in the file
        terraform_file = get_data(test_resource_paths.terraform_orphan_component)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the VPCsmm components without parents are omitted
        # AND the rest of the OTM details match the expected
        assert validate_and_diff_otm(otm.json(), expected_orphan_component_is_not_mapped, excluded_regex) == {}


    def test_run_valid_mappings(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_for_mappings_tests_json)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'

        assert otm.components[0].type == 'vpc'
        assert otm.components[0].name == 'vpc'
        assert otm.components[0].parent_type == 'trustZone'

        assert otm.components[1].type == 'ec2'
        assert otm.components[1].name == 'inst'
        assert otm.components[1].parent_type == 'trustZone'

        assert otm.components[2].type == 'empty-component'
        assert otm.components[2].name == 'subnet_1'
        assert otm.components[2].parent_type == 'component'

        assert otm.components[3].type == 'empty-component'
        assert otm.components[3].name == 'subnet_2'
        assert otm.components[3].parent_type == 'component'

    def test_aws_dataflows(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_dataflows)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 9
        assert len(otm.dataflows) == 5

        # AND the info inside them is also right
        assert_otm_trustzone(otm, 0, PUBLIC_CLOUD_TZ_ID, "Public Cloud")

        assert_otm_component(otm, 0, 'dynamodb', 'basic_dynamodb_table', PUBLIC_CLOUD_TZ_ID, ['aws_dynamodb_table'])
        assert_otm_component(otm, 1, 'aws-lambda-function', 'basic_lambda', PUBLIC_CLOUD_TZ_ID,
                             ['aws_lambda_function'])
        assert_otm_component(otm, 2, 's3', 'log_bucket_deprecated', PUBLIC_CLOUD_TZ_ID, ['aws_s3_bucket'])
        assert_otm_component(otm, 3, 's3', 'bucket_deprecated', PUBLIC_CLOUD_TZ_ID, ['aws_s3_bucket'])
        assert_otm_component(otm, 4, 's3', 'log_bucket', PUBLIC_CLOUD_TZ_ID, ['aws_s3_bucket'])
        assert_otm_component(otm, 5, 's3', 'bucket', PUBLIC_CLOUD_TZ_ID, ['aws_s3_bucket'])
        assert_otm_component(otm, 6, 'sqs-simple-queue-service', 'failure_queue', PUBLIC_CLOUD_TZ_ID,
                             ['aws_sqs_queue'])
        assert_otm_component(otm, 7, 'cognito', 'user_pool', PUBLIC_CLOUD_TZ_ID, ['aws_cognito_user_pool'])
        assert_otm_component(otm, 8, 'api-gateway', 'api-gateway (grouped)', PUBLIC_CLOUD_TZ_ID,
                             ['rest_api (aws_api_gateway_rest_api)',
                              'api_authorizer (aws_api_gateway_authorizer)'])

        assert_otm_dataflow(otm, 0, otm.components[0].id, otm.components[1].id,
                            'dataflow to Lambda function in basic_dynamodb_event')
        assert_otm_dataflow(otm, 1, otm.components[1].id, otm.components[6].id,
                            'dataflow from Lambda function on Failure basic_dynamodb_event')
        assert_otm_dataflow(otm, 2, otm.components[3].id, otm.components[2].id, 'S3 dataflow from bucket_deprecated')
        assert_otm_dataflow(otm, 3, otm.components[5].id, otm.components[4].id,
                            'S3 dataflow from aws_s3_bucket_logging')
        assert_otm_dataflow(otm, 4, otm.components[8].id, otm.components[7].id,
                            'API gateway data flow from aws_api_gateway_authorizer')

    def test_aws_parent_children_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_parent_children_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 2

        # AND the info inside them is also right
        assert_otm_component(otm, 0, 'elastic-container-service', 'mongo', PUBLIC_CLOUD_TZ_ID, ['aws_ecs_service'])
        assert_otm_component(otm, 1, 'docker-container', 'service', otm.components[0].id, ['aws_ecs_task_definition'])

    def test_aws_singleton_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_singleton_components_unix_line_breaks)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 20
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert_otm_component(otm, 0, 'CD-ACM', 'acm_certificate', PUBLIC_CLOUD_TZ_ID, ['aws_acm_certificate'])
        assert_otm_component(otm, 1, 'cloudwatch', 'cloudwatch (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'cloudwatch_metric_alarm_1 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_metric_alarm_2 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_log_group_1 (aws_cloudwatch_log_group)',
            'cloudwatch_log_group_2 (aws_cloudwatch_log_group)'
        ])
        assert_otm_component(otm, 2, 'kms', 'kms_key', PUBLIC_CLOUD_TZ_ID, ['aws_kms_key'])
        assert_otm_component(otm, 3, 'CD-SECRETS-MANAGER', 'CD-SECRETS-MANAGER (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'secretsmanager_secret_1 (aws_secretsmanager_secret)',
            'secretsmanager_secret_2 (aws_secretsmanager_secret)'
        ])
        assert_otm_component(otm, 4, 'CD-SYSTEMS-MANAGER', 'CD-SYSTEMS-MANAGER (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'ssm_parameter (aws_ssm_parameter)',
            'ssm_document (aws_ssm_document)'
        ])
        assert_otm_component(otm, 5, 'api-gateway', 'api-gateway (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'api_gateway_api_key (aws_api_gateway_api_key)',
            'api_gateway_client_certificate (aws_api_gateway_client_certificate)'
        ])
        assert_otm_component(otm, 6, 'athena', 'athena (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'athena_workgroup (aws_athena_workgroup)',
            'athena_database (aws_athena_database)'
        ])
        assert_otm_component(otm, 7, 'CD-MQ', 'CD-MQ (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'mq_broker (aws_mq_broker)',
            'mq_configuration (aws_mq_configuration)'
        ])
        assert_otm_component(otm, 8, 'cf-cloudfront', 'cf-cloudfront (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'cloudfront_origin_access_identity (aws_cloudfront_origin_access_identity)',
            'cloudfront_public_key (aws_cloudfront_public_key)'
        ])
        assert_otm_component(otm, 9, 'CD-CONFIG', 'CD-CONFIG (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'config_config_rule (aws_config_config_rule)',
            'config_configuration_recorder (aws_config_configuration_recorder)'
        ])
        assert_otm_component(otm, 10, 'elastic-container-registry', 'elastic-container-registry (grouped)',
                             PUBLIC_CLOUD_TZ_ID,
                             [
                                 'ecr_repository (aws_ecr_repository)',
                                 'ecr_lifecycle_policy (aws_ecr_lifecycle_policy)'
                             ])
        assert_otm_component(otm, 11, 'elasticache', 'elasticache (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'elasticache_user (aws_elasticache_user)',
            'elasticache_user_group (aws_elasticache_user_group)'
        ])
        assert_otm_component(otm, 12, 'CD-GUARDDUTY', 'CD-GUARDDUTY (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'guardduty_detector_1 (aws_guardduty_detector)',
            'guardduty_detector_2 (aws_guardduty_detector)'
        ])
        assert_otm_component(otm, 13, 'CD-INSPECTOR', 'CD-INSPECTOR (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'inspector_resource_group (aws_inspector_resource_group)',
            'inspector_assessment_target (aws_inspector_assessment_target)'
        ])
        assert_otm_component(otm, 14, 'CD-MACIE', 'CD-MACIE (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'macie2_account (aws_macie2_account)',
            'macie2_member (aws_macie2_member)'
        ])
        assert_otm_component(otm, 15, 'CD-SES', 'CD-SES (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'ses_receipt_filter (aws_ses_receipt_filter)',
            'ses_receipt_rule (aws_ses_receipt_rule)'
        ])
        assert_otm_component(otm, 16, 'sns', 'sns (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'sns_topic (aws_sns_topic)',
            'sns_topic_subscription (aws_sns_topic_subscription)'
        ])
        assert_otm_component(otm, 17, 'CD-WAF', 'CD-WAF (grouped)', PUBLIC_CLOUD_TZ_ID, [
            'waf_ipset (aws_waf_ipset)',
            'waf_rule (aws_waf_rule)'
        ])
        assert_otm_component(otm, 18, 'kinesis-data-analytics', 'kinesis-data-analytics (grouped)',
                             PUBLIC_CLOUD_TZ_ID, [
                                 'kinesis_analytics_application_1 (aws_kinesis_analytics_application)',
                                 'kinesis_analytics_application_2 (aws_kinesis_analytics_application)',
                                 'kinesis_stream (aws_kinesis_stream)',
                                 'kinesis_stream_consumer (aws_kinesis_stream_consumer)'
                             ])
        assert_otm_component(otm, 19, 'kinesis-data-firehose', 'kinesis-data-firehose (grouped)', PUBLIC_CLOUD_TZ_ID,
                             [
                                 'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)',
                                 'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)'
                             ])

    def test_aws_altsource_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_altsource_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 9

        # AND the info inside them is also right
        assert_otm_component(otm, 0, 'dynamodb', 'DynamoDB from VPCEndpoint', None,
                             ['dynamodb (aws_vpc_endpoint)'])
        assert_otm_component(otm, 1, 'empty-component', 'ssm', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 2, 'empty-component', 'ssm_messages', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 3, 'empty-component', 'ecr', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 4, 'empty-component', 'dynamodb', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 5, 'empty-component', 's3', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 6, 's3', 'S3 from VPCEndpoint', None, ['s3 (aws_vpc_endpoint)'])
        assert_otm_component(otm, 7, 'CD-SYSTEMS-MANAGER', 'Systems Manager from VPCEndpoint (grouped)', None,
                             ['ssm (aws_vpc_endpoint)', 'ssm_messages (aws_vpc_endpoint)'])
        assert_otm_component(otm, 8, 'elastic-container-registry', 'ECR from VPCEndpoint', None,
                             ['ecr (aws_vpc_endpoint)'])

    def test_aws_security_groups_components(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_security_groups_components)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 22
        assert len(otm.dataflows) == 22

        # AND the info inside them is also right
        assert_otm_trustzone(otm, 0, PUBLIC_CLOUD_TZ_ID, "Public Cloud")
        assert_otm_trustzone(otm, 1, INTERNET_TZ_ID, "Internet")

        assert_otm_component(otm, 0, 'vpc', 'CustomVPC', PUBLIC_CLOUD_TZ_ID, ['aws_vpc'])
        assert_otm_component(otm, 1, 'empty-component', 'PrivateSubnet1', otm.components[0].id, ['aws_subnet'])
        assert_otm_component(otm, 2, 'empty-component', 'PrivateSubnet2', otm.components[0].id, ['aws_subnet'])
        assert_otm_component(otm, 3, 'empty-component', 'PublicSubnet1', otm.components[0].id, ['aws_subnet'])
        assert_otm_component(otm, 4, 'empty-component', 'PublicSubnet2', otm.components[0].id, ['aws_subnet'])
        assert_otm_component(otm, 5, 'empty-component', 'VPCssm', otm.components[1].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 6, 'empty-component', 'VPCssm', otm.components[2].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 7, 'empty-component', 'VPCssmmessages', otm.components[1].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 8, 'empty-component', 'VPCssmmessages', otm.components[2].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 9, 'empty-component', 'VPCmonitoring', otm.components[1].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 10, 'empty-component', 'VPCmonitoring', otm.components[2].id, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 11, 'elastic-container-service', 'Service', otm.components[1].id, ['aws_ecs_service'])
        assert_otm_component(otm, 12, 'elastic-container-service', 'Service', otm.components[2].id, ['aws_ecs_service'])
        assert_otm_component(otm, 13, 'docker-container', 'ServiceTaskDefinition', otm.components[11].id,
                             ['aws_ecs_task_definition'])
        assert_otm_component(otm, 14, 'docker-container', 'ServiceTaskDefinition', otm.components[12].id,
                             ['aws_ecs_task_definition'])
        assert_otm_component(otm, 15, 'load-balancer', 'ServiceLB', otm.components[1].id, ['aws_lb'])
        assert_otm_component(otm, 16, 'load-balancer', 'ServiceLB', otm.components[2].id, ['aws_lb'])
        assert_otm_component(otm, 17, 'empty-component', 'Canary', otm.components[3].id, ['aws_synthetics_canary'])
        assert_otm_component(otm, 18, 'empty-component', 'Canary', otm.components[4].id, ['aws_synthetics_canary'])
        assert_otm_component(otm, 19, 'generic-client', '0.0.0.0/0', INTERNET_TZ_ID,
                             ['Outbound connection destination IP'])
        assert_otm_component(otm, 20, 'generic-client', '255.255.255.255/32', INTERNET_TZ_ID,
                             ['Outbound connection destination IP'])
        assert_otm_component(otm, 21, 'CD-SYSTEMS-MANAGER', 'Systems Manager from VPCEndpoint (grouped)',
                             PUBLIC_CLOUD_TZ_ID,
                             ['VPCssm (aws_vpc_endpoint)', 'VPCssmmessages (aws_vpc_endpoint)'])

        assert_otm_dataflow(otm, 0, otm.components[0].id, otm.components[5].id, 'VPCssmSecurityGroup -> VPCssm')
        assert_otm_dataflow(otm, 1, otm.components[5].id, otm.components[19].id, 'VPCssm -> VPCssmSecurityGroup')
        assert_otm_dataflow(otm, 2, otm.components[0].id, otm.components[6].id, 'VPCssmSecurityGroup -> VPCssm')
        assert_otm_dataflow(otm, 3, otm.components[6].id, otm.components[19].id, 'VPCssm -> VPCssmSecurityGroup')
        assert_otm_dataflow(otm, 4, otm.components[0].id, otm.components[7].id,
                            'VPCssmmessagesSecurityGroup -> VPCssmmessages')
        assert_otm_dataflow(otm, 5, otm.components[7].id, otm.components[19].id,
                            'VPCssmmessages -> VPCssmmessagesSecurityGroup')
        assert_otm_dataflow(otm, 6, otm.components[0].id, otm.components[8].id,
                            'VPCssmmessagesSecurityGroup -> VPCssmmessages')
        assert_otm_dataflow(otm, 7, otm.components[8].id, otm.components[19].id,
                            'VPCssmmessages -> VPCssmmessagesSecurityGroup')
        assert_otm_dataflow(otm, 8, otm.components[0].id, otm.components[9].id,
                            'VPCmonitoringSecurityGroup -> VPCmonitoring')
        assert_otm_dataflow(otm, 9, otm.components[9].id, otm.components[19].id,
                            'VPCmonitoring -> VPCmonitoringSecurityGroup')
        assert_otm_dataflow(otm, 10, otm.components[0].id, otm.components[10].id,
                            'VPCmonitoringSecurityGroup -> VPCmonitoring')
        assert_otm_dataflow(otm, 11, otm.components[10].id, otm.components[19].id,
                            'VPCmonitoring -> VPCmonitoringSecurityGroup')
        assert_otm_dataflow(otm, 12, otm.components[11].id, otm.components[20].id, 'Service -> OutboundSecurityGroup')
        assert_otm_dataflow(otm, 13, otm.components[12].id, otm.components[20].id, 'Service -> OutboundSecurityGroup')
        assert_otm_dataflow(otm, 14, otm.components[15].id, otm.components[11].id, 'ServiceLB -> Service')
        assert_otm_dataflow(otm, 15, otm.components[15].id, otm.components[12].id, 'ServiceLB -> Service')
        assert_otm_dataflow(otm, 16, otm.components[17].id, otm.components[15].id, 'Canary -> ServiceLB')
        assert_otm_dataflow(otm, 17, otm.components[18].id, otm.components[15].id, 'Canary -> ServiceLB')
        assert_otm_dataflow(otm, 18, otm.components[16].id, otm.components[11].id, 'ServiceLB -> Service')
        assert_otm_dataflow(otm, 19, otm.components[16].id, otm.components[12].id, 'ServiceLB -> Service')
        assert_otm_dataflow(otm, 20, otm.components[17].id, otm.components[16].id, 'Canary -> ServiceLB')
        assert_otm_dataflow(otm, 21, otm.components[18].id, otm.components[16].id, 'Canary -> ServiceLB')

    def test_mapping_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_component_without_parent)

        # AND an invalid TF mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        # THEN an OtmBuildingError is raised
        with pytest.raises(OtmBuildingError) as e_info:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # AND the error references a parent issue
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    def test_mapping_skipped_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_skipped_component_without_parent)

        # AND a TF mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 1
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'
        assert otm.components[0].type == 'aws_control'
        assert otm.components[0].name == 'Control_component'
        assert otm.components[0].parent == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

    def test_no_resources(self):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_no_resources)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.default_terraform_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        assert otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].name == 'Public Cloud'

    def test_mapping_modules(self):
        # GIVEN a valid TF file with some TF modules
        terraform_file = get_data(test_resource_paths.terraform_modules)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        aws_rds_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/rds/aws')
        assert aws_rds_modules[0].name == 'db23test'
        assert aws_rds_modules[0].parent_type == 'trustZone'
        assert aws_rds_modules[0].source['source'] == 'terraform-aws-modules/rds/aws'

    def test_extra_modules(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_extra_modules_sample)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_mapping_extra_modules)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 0

        # AND the info inside them is also right
        rds_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/rds/aws')
        vpc_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/vpc/aws')
        load_balancer_modules = utils.filter_modules_by_type(otm.components, 'terraform-aws-modules/alb/aws')

        assert len(rds_modules) == 1
        assert len(vpc_modules) == 1
        assert len(load_balancer_modules) == 1

        assert rds_modules[0].source['source'] == 'terraform-aws-modules/rds/aws'
        assert vpc_modules[0].source['source'] == 'terraform-aws-modules/vpc/aws'
        assert load_balancer_modules[0].source['source'] == 'terraform-aws-modules/alb/aws'

    @pytest.mark.parametrize('mapping_file', [None, [None]])
    def test_mapping_files_not_provided(self, mapping_file):
        # GIVEN a sample valid IaC file (and none mapping file)
        terraform_file = [get_data(SAMPLE_VALID_TF_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises TypeError
        with pytest.raises(TypeError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [get_data(mapping_file)]).process()

    def test_invalid_mapping_files(self):
        # GIVEN a sample valid IaC file
        terraform_file = get_data(SAMPLE_VALID_TF_FILE)

        # AND an invalid iac mappings file
        mapping_file = [get_data(test_resource_paths.invalid_yaml)]

        # WHEN creating OTM project from IaC file
        # THEN raises MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    def test_invalid_terraform_file(self):
        # Given a sample invalid TF file
        terraform_file = [get_data(test_resource_paths.invalid_tf)]

        # And a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # When creating OTM project from IaC file
        # Then raises OtmBuildingError
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], mapping_file).process()

    def test_elb_example(self):
        # GIVEN a valid TF file with some special TF modules
        terraform_file = get_data(test_resource_paths.terraform_elb)

        # AND a valid TF mapping file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 0

        assert_otm_component(otm, 0, 'vpc', 'foo', PUBLIC_CLOUD_TZ_ID, ['aws_vpc'])
        assert_otm_component(otm, 1, 'empty-component', 'baz', otm.components[0].id, ['aws_subnet'])
        assert_otm_component(otm, 2, 'empty-component', 'bar', otm.components[0].id, ['aws_subnet'])

        assert otm.components[0].id != otm.components[1].id
        assert otm.components[1].id != otm.components[2].id

    # Parse a Simple IaC file
    def test_process_single_tf_file(self):
        # GIVEN the single tf file
        terraform_file = get_data(test_resource_paths.terraform_single_tf)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        assert validate_and_diff_otm(otm.json(), test_resource_paths.tf_file_expected_result, excluded_regex) == {}

    # Parse a Multiple IaC file
    def test_process_multiple_tf_file(self):
        # GIVEN the multiples tf file
        terraform_networks = get_data(test_resource_paths.terraform_networks)
        terraform_resources = get_data(test_resource_paths.terraform_resources)

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        otm = TerraformProcessor(
            SAMPLE_ID, SAMPLE_NAME, [terraform_networks, terraform_resources], [mapping_file]
        ).process()

        # THEN a file with the single_tf_file-expected-result.otm contents is returned
        assert validate_and_diff_otm(otm.json(), test_resource_paths.tf_file_expected_result, excluded_regex) == {}

    # Parse an empty Array IaC file
    def test_process_empty_source_file_array(self):
        # GIVEN an empty array IaC file
        terraform_empty_iac_array = []

        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN the method TerraformProcessor::process is invoked
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(LoadingIacFileError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, terraform_empty_iac_array, [mapping_file]).process()

    @pytest.mark.parametrize('source', [
        # GIVEN a request with one iac_file keys with no value
        [get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with all iac_file keys with no value
        [get_data(test_resource_paths.terraform_invalid_size),
         get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with no value
        [get_data(test_resource_paths.terraform_single_tf),
         get_data(test_resource_paths.terraform_invalid_size)],
        # GIVEN a request with some iac_file keys with invalid format
        [get_data(test_resource_paths.terraform_single_tf),
         get_byte_data(test_resource_paths.terraform_gz)]
    ])
    def test_mapping_files_not_provided(self, source):
        # AND the iriusrisk-tf-aws-mapping.yaml file
        mapping_file = get_data(test_resource_paths.terraform_iriusrisk_tf_aws_mapping)

        # WHEN creating OTM project from IaC file
        # THEN an LoadingIacFileError  is returned
        with pytest.raises(IacFileNotValidError):
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, source, [mapping_file]).process()

    def test_minimal_tf_file(self):
        # Given a minimal valid TF file
        terraform_minimal_file = get_data(test_resource_paths.terraform_minimal_content)

        # and the default mapping file for TF
        mapping_file = get_data(test_resource_paths.default_terraform_mapping)

        # When parsing the file with Startleft and the default mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_minimal_file], [mapping_file]).process()

        # Then an empty OTM containing only the default trustzone is generated
        assert validate_and_diff_otm(otm.json(), test_resource_paths.otm_with_only_default_trustzone_expected_result,
                                     excluded_regex) == {}

    def test_generate_empty_otm_with_empty_mapping_file(self):
        # Given an empty mapping file
        mapping_file = get_data(test_resource_paths.empty_terraform_mapping)

        # and a valid TF file with content
        terraform_file = get_data(test_resource_paths.terraform_aws_simple_components)

        # When parsing the file with Startleft and the empty mapping file
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # Then an empty OTM, without any threat modeling content, is generated
        assert validate_and_diff_otm(otm.json(), test_resource_paths.minimal_otm_expected_result,
                                     excluded_regex) == {}
