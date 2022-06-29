import pytest

from startleft.iac.iac_to_otm import IacToOtm
from startleft.iac.iac_type import IacType
from startleft.utils.file_utils import FileUtils
from tests.resources import test_resource_paths


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


class TestTerraformAWSComponents:
    public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
    internet_id = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

    def test_aws_multiple_components(self):
        filename = test_resource_paths.terraform_aws_multiple_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS simple components', 'aws_simple_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 21
        assert_otm_component(otm, 0, 'empty-component', 'gw', self.public_cloud_id, ['aws_internet_gateway'])
        assert_otm_component(otm, 1, 'elastic-container-service', 'mongo', self.public_cloud_id, ['aws_ecs_service'])
        assert_otm_component(otm, 2, 'docker-container', 'service', self.public_cloud_id, ['aws_ecs_task_definition'])
        assert_otm_component(otm, 3, 'docker-container', 'service_task', self.public_cloud_id, ['aws_ecs_task_definition'])
        assert_otm_component(otm, 4, 'load-balancer', 'lb', None, ['aws_lb'])
        assert_otm_component(otm, 5, 'load-balancer', 'wu-tang', None, ['aws_elb'])
        assert_otm_component(otm, 6, 'aws-lambda-function', 'test_lambda', self.public_cloud_id, ['aws_lambda_function'])
        assert_otm_component(otm, 7, 'rds', 'mysql', self.public_cloud_id, ['aws_db_instance'])
        assert_otm_component(otm, 8, 'rds', 'aurora-cluster-demo', self.public_cloud_id, ['aws_rds_cluster'])
        assert_otm_component(otm, 9, 'route-53', 'route-53-zone-example', self.public_cloud_id, ['aws_route53_zone'])
        assert_otm_component(otm, 10, 's3', 'foo_s3_bucket', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm_component(otm, 11, 'sqs-simple-queue-service', 'terraform_queue', self.public_cloud_id, ['aws_sqs_queue'])
        assert_otm_component(otm, 12, 'empty-component', 'some-canary', self.public_cloud_id, ['aws_synthetics_canary'])
        assert_otm_component(otm, 13, 'cloudtrail', 'foobar', self.public_cloud_id, ['aws_cloudtrail'])
        assert_otm_component(otm, 14, 'cognito', 'pool', self.public_cloud_id, ['aws_cognito_user_pool'])
        assert_otm_component(otm, 15, 'cognito', 'main', self.public_cloud_id, ['aws_cognito_identity_pool'])
        assert_otm_component(otm, 16, 'elastic-container-kubernetes', 'example', self.public_cloud_id, ['aws_eks_cluster'])
        assert_otm_component(otm, 17, 'CD-AWS-NETWORK-FIREWALL', 'firewall_example', None,
                             ['aws_networkfirewall_firewall'])
        assert_otm_component(otm, 18, 'redshift', 'tf-redshift-cluster', self.public_cloud_id, ['aws_redshift_cluster'])
        assert_otm_component(otm, 19, 'step-functions', 'my_sfn_activity', self.public_cloud_id, ['aws_sfn_activity'])
        assert_otm_component(otm, 20, 'step-functions', 'my_sfn_state_machine', self.public_cloud_id, ['aws_sfn_state_machine'])

    def test_aws_parent_children_components(self):
        filename = test_resource_paths.terraform_aws_parent_children_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm(
            'Test case AWS with $parent and $children components',
            'aws_parent_children_components',
            IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 2
        assert_otm_component(otm, 0, 'elastic-container-service', 'mongo', self.public_cloud_id, ['aws_ecs_service'])
        assert_otm_component(otm, 1, 'docker-container', 'service', otm.components[0].id, ['aws_ecs_task_definition'])

    @pytest.mark.parametrize('filename, break_line', [
        (test_resource_paths.terraform_aws_singleton_components_unix_line_breaks, '\n'),
        (test_resource_paths.terraform_aws_singleton_components_unix_line_breaks, '\r\n'),
        (test_resource_paths.terraform_aws_singleton_components_unix_line_breaks, '\r')
    ])
    def test_aws_singleton_components(self, filename: str, break_line: str):
        iac_data = FileUtils.get_byte_data(filename).decode().replace('\n', break_line)
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS singleton components', 'aws_singleton_components', IacType.TERRAFORM)

        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [iac_data])

        assert break_line in iac_data
        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 20
        assert len(otm.dataflows) == 0
        assert_otm_component(otm, 0, 'CD-ACM', 'acm_certificate', self.public_cloud_id, ['aws_acm_certificate'])
        assert_otm_component(otm, 1, 'cloudwatch', 'cloudwatch (grouped)', self.public_cloud_id, [
            'cloudwatch_metric_alarm_1 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_metric_alarm_2 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_log_group_1 (aws_cloudwatch_log_group)',
            'cloudwatch_log_group_2 (aws_cloudwatch_log_group)'
        ])
        assert_otm_component(otm, 2, 'kms', 'kms_key', self.public_cloud_id, ['aws_kms_key'])
        assert_otm_component(otm, 3, 'CD-SECRETS-MANAGER', 'CD-SECRETS-MANAGER (grouped)', self.public_cloud_id, [
            'secretsmanager_secret_1 (aws_secretsmanager_secret)',
            'secretsmanager_secret_2 (aws_secretsmanager_secret)'
        ])
        assert_otm_component(otm, 4, 'CD-SYSTEMS-MANAGER', 'CD-SYSTEMS-MANAGER (grouped)', self.public_cloud_id, [
            'ssm_parameter (aws_ssm_parameter)',
            'ssm_document (aws_ssm_document)'
        ])
        assert_otm_component(otm, 5, 'api-gateway', 'api-gateway (grouped)', self.public_cloud_id, [
            'api_gateway_api_key (aws_api_gateway_api_key)',
            'api_gateway_client_certificate (aws_api_gateway_client_certificate)'
        ])
        assert_otm_component(otm, 6, 'athena', 'athena (grouped)', self.public_cloud_id, [
            'athena_workgroup (aws_athena_workgroup)',
            'athena_database (aws_athena_database)'
        ])
        assert_otm_component(otm, 7, 'CD-MQ', 'CD-MQ (grouped)', self.public_cloud_id, [
            'mq_broker (aws_mq_broker)',
            'mq_configuration (aws_mq_configuration)'
        ])
        assert_otm_component(otm, 8, 'cf-cloudfront', 'cf-cloudfront (grouped)', self.public_cloud_id, [
            'cloudfront_origin_access_identity (aws_cloudfront_origin_access_identity)',
            'cloudfront_public_key (aws_cloudfront_public_key)'
        ])
        assert_otm_component(otm, 9, 'CD-CONFIG', 'CD-CONFIG (grouped)', self.public_cloud_id, [
            'config_config_rule (aws_config_config_rule)',
            'config_configuration_recorder (aws_config_configuration_recorder)'
        ])
        assert_otm_component(otm, 10, 'elastic-container-registry', 'elastic-container-registry (grouped)', self.public_cloud_id,
                             [
                       'ecr_repository (aws_ecr_repository)',
                       'ecr_lifecycle_policy (aws_ecr_lifecycle_policy)'
                   ])
        assert_otm_component(otm, 11, 'elasticache', 'elasticache (grouped)', self.public_cloud_id, [
            'elasticache_user (aws_elasticache_user)',
            'elasticache_user_group (aws_elasticache_user_group)'
        ])
        assert_otm_component(otm, 12, 'CD-GUARDDUTY', 'CD-GUARDDUTY (grouped)', self.public_cloud_id, [
            'guardduty_detector_1 (aws_guardduty_detector)',
            'guardduty_detector_2 (aws_guardduty_detector)'
        ])
        assert_otm_component(otm, 13, 'CD-INSPECTOR', 'CD-INSPECTOR (grouped)', self.public_cloud_id, [
            'inspector_resource_group (aws_inspector_resource_group)',
            'inspector_assessment_target (aws_inspector_assessment_target)'
        ])
        assert_otm_component(otm, 14, 'CD-MACIE', 'CD-MACIE (grouped)', self.public_cloud_id, [
            'macie2_account (aws_macie2_account)',
            'macie2_member (aws_macie2_member)'
        ])
        assert_otm_component(otm, 15, 'CD-SES', 'CD-SES (grouped)', self.public_cloud_id, [
            'ses_receipt_filter (aws_ses_receipt_filter)',
            'ses_receipt_rule (aws_ses_receipt_rule)'
        ])
        assert_otm_component(otm, 16, 'sns', 'sns (grouped)', self.public_cloud_id, [
            'sns_topic (aws_sns_topic)',
            'sns_topic_subscription (aws_sns_topic_subscription)'
        ])
        assert_otm_component(otm, 17, 'CD-WAF', 'CD-WAF (grouped)', self.public_cloud_id, [
            'waf_ipset (aws_waf_ipset)',
            'waf_rule (aws_waf_rule)'
        ])
        assert_otm_component(otm, 18, 'kinesis-data-analytics', 'kinesis-data-analytics (grouped)', self.public_cloud_id, [
            'kinesis_analytics_application_1 (aws_kinesis_analytics_application)',
            'kinesis_analytics_application_2 (aws_kinesis_analytics_application)',
            'kinesis_stream (aws_kinesis_stream)',
            'kinesis_stream_consumer (aws_kinesis_stream_consumer)'
        ])
        assert_otm_component(otm, 19, 'kinesis-data-firehose', 'kinesis-data-firehose (grouped)', self.public_cloud_id, [
            'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)',
            'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)'
        ])

    def test_aws_altsource_components(self):
        filename = test_resource_paths.terraform_aws_altsource_components
        iac_data = FileUtils.get_byte_data(filename).decode()
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS altsource components', 'aws_altsource_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [iac_data])

        assert iac_to_otm.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 13
        assert_otm_component(otm, 0, 'dynamodb', 'DynamoDB from VPCEndpoint', None,
                             ['dynamodb (aws_vpc_endpoint)'])
        assert_otm_component(otm, 1, 'empty-component', 'subnets', None, ['aws_subnet'])
        assert_otm_component(otm, 2, 'empty-component', 'ec2', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 3, 'empty-component', 'ec2_messages', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 4, 'empty-component', 'ssm', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 5, 'empty-component', 'ssm_messages', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 6, 'empty-component', 'ecr', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 7, 'empty-component', 'dynamodb', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 8, 'empty-component', 's3', None, ['aws_vpc_endpoint'])
        assert_otm_component(otm, 9, 's3', 'S3 from VPCEndpoint', None, ['s3 (aws_vpc_endpoint)'])
        assert_otm_component(otm, 10, 'generic-client', '0.0.0.0/0', None,
                             ['Inbound connection source IP'])
        assert_otm_component(otm, 11, 'CD-SYSTEMS-MANAGER', 'Systems Manager from VPCEndpoint (grouped)', None,
                             [
                       'ssm (aws_vpc_endpoint)',
                       'ssm_messages (aws_vpc_endpoint)'
                   ])
        assert_otm_component(otm, 12, 'elastic-container-registry', 'ECR from VPCEndpoint', None,
                             ['ecr (aws_vpc_endpoint)'])

    def test_aws_security_groups_components(self):
        filename = test_resource_paths.terraform_aws_security_groups_components
        iac_data = FileUtils.get_byte_data(filename).decode()
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS security groups components', 'aws_security_groups_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [iac_data])

        otm = iac_to_otm.otm

        assert iac_to_otm.otm
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 22
        assert len(otm.dataflows) == 22

        assert_otm_trustzone(otm, 0, self.public_cloud_id, "Public Cloud")
        assert_otm_trustzone(otm, 1, self.internet_id, "Internet")

        assert_otm_component(otm, 0, 'vpc', 'CustomVPC', self.public_cloud_id, ['aws_vpc'])
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
        assert_otm_component(otm, 13, 'docker-container', 'ServiceTaskDefinition', otm.components[11].id, ['aws_ecs_task_definition'])
        assert_otm_component(otm, 14, 'docker-container', 'ServiceTaskDefinition', otm.components[12].id, ['aws_ecs_task_definition'])
        assert_otm_component(otm, 15, 'load-balancer', 'ServiceLB', otm.components[1].id, ['aws_lb'])
        assert_otm_component(otm, 16, 'load-balancer', 'ServiceLB', otm.components[2].id, ['aws_lb'])
        assert_otm_component(otm, 17, 'empty-component', 'Canary', otm.components[3].id, ['aws_synthetics_canary'])
        assert_otm_component(otm, 18, 'empty-component', 'Canary', otm.components[4].id, ['aws_synthetics_canary'])
        assert_otm_component(otm, 19, 'generic-client', '0.0.0.0/0', self.internet_id, ['Outbound connection destination IP'])
        assert_otm_component(otm, 20, 'generic-client', '255.255.255.255/32', self.internet_id, ['Outbound connection destination IP'])
        assert_otm_component(otm, 21, 'CD-SYSTEMS-MANAGER', 'Systems Manager from VPCEndpoint (grouped)', self.public_cloud_id,
                             ['VPCssm (aws_vpc_endpoint)', 'VPCssmmessages (aws_vpc_endpoint)'])

        assert_otm_dataflow(otm, 0, otm.components[0].id, otm.components[5].id, 'VPCssmSecurityGroup -> VPCssm')
        assert_otm_dataflow(otm, 1, otm.components[5].id, otm.components[19].id, 'VPCssm -> VPCssmSecurityGroup')
        assert_otm_dataflow(otm, 2, otm.components[0].id, otm.components[6].id, 'VPCssmSecurityGroup -> VPCssm')
        assert_otm_dataflow(otm, 3, otm.components[6].id, otm.components[19].id, 'VPCssm -> VPCssmSecurityGroup')
        assert_otm_dataflow(otm, 4, otm.components[0].id, otm.components[7].id, 'VPCssmmessagesSecurityGroup -> VPCssmmessages')
        assert_otm_dataflow(otm, 5, otm.components[7].id, otm.components[19].id, 'VPCssmmessages -> VPCssmmessagesSecurityGroup')
        assert_otm_dataflow(otm, 6, otm.components[0].id, otm.components[8].id, 'VPCssmmessagesSecurityGroup -> VPCssmmessages')
        assert_otm_dataflow(otm, 7, otm.components[8].id, otm.components[19].id, 'VPCssmmessages -> VPCssmmessagesSecurityGroup')
        assert_otm_dataflow(otm, 8, otm.components[0].id, otm.components[9].id, 'VPCmonitoringSecurityGroup -> VPCmonitoring')
        assert_otm_dataflow(otm, 9, otm.components[9].id, otm.components[19].id, 'VPCmonitoring -> VPCmonitoringSecurityGroup')
        assert_otm_dataflow(otm, 10, otm.components[0].id, otm.components[10].id, 'VPCmonitoringSecurityGroup -> VPCmonitoring')
        assert_otm_dataflow(otm, 11, otm.components[10].id, otm.components[19].id, 'VPCmonitoring -> VPCmonitoringSecurityGroup')
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

    def test_aws_dataflows(self):
        filename = test_resource_paths.terraform_aws_dataflows
        iac_data = FileUtils.get_byte_data(filename).decode()
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS dataflows', 'aws_dataflows', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, [FileUtils.get_data(mapping_filename)], [iac_data])

        otm = iac_to_otm.otm

        assert iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 9
        assert len(otm.dataflows) == 5

        assert_otm_trustzone(otm, 0, self.public_cloud_id, "Public Cloud")

        assert_otm_component(otm, 0, 'dynamodb', 'basic_dynamodb_table', self.public_cloud_id, ['aws_dynamodb_table'])
        assert_otm_component(otm, 1, 'aws-lambda-function', 'basic_lambda', self.public_cloud_id, ['aws_lambda_function'])
        assert_otm_component(otm, 2, 's3', 'log_bucket_deprecated', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm_component(otm, 3, 's3', 'bucket_deprecated', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm_component(otm, 4, 's3', 'log_bucket', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm_component(otm, 5, 's3', 'bucket', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm_component(otm, 6, 'sqs-simple-queue-service', 'failure_queue', self.public_cloud_id, ['aws_sqs_queue'])
        assert_otm_component(otm, 7, 'cognito', 'user_pool', self.public_cloud_id, ['aws_cognito_user_pool'])
        assert_otm_component(otm, 8, 'api-gateway', 'api-gateway (grouped)', self.public_cloud_id,
                             ['rest_api (aws_api_gateway_rest_api)',
                              'api_authorizer (aws_api_gateway_authorizer)'])

        assert_otm_dataflow(otm, 0, otm.components[0].id, otm.components[1].id, 'dataflow to Lambda function in basic_dynamodb_event')
        assert_otm_dataflow(otm, 1, otm.components[1].id, otm.components[6].id, 'dataflow from Lambda function on Failure basic_dynamodb_event')
        assert_otm_dataflow(otm, 2, otm.components[3].id, otm.components[2].id, 'S3 dataflow from bucket_deprecated')
        assert_otm_dataflow(otm, 3, otm.components[5].id, otm.components[4].id, 'S3 dataflow from aws_s3_bucket_logging')
        assert_otm_dataflow(otm, 4, otm.components[8].id, otm.components[7].id, 'API gateway data flow from aws_api_gateway_authorizer')
