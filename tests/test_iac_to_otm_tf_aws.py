from startleft.api.controllers.iac.iac_type import IacType
from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


def assert_otm(otm, position, c_type, c_name, c_parent, c_tags):
    assert otm.components[position].type == c_type
    assert otm.components[position].name == c_name
    assert otm.components[position].parent == c_parent
    for c_tag in c_tags:
        assert c_tag in otm.components[position].tags


class TestTerraformAWSComponents:
    public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

    def test_aws_simple_components(self):
        filename = test_resource_paths.terraform_aws_simple_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS simple components', 'aws_simple_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-simple-terraform.otm', filename)

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 21
        assert_otm(otm, 0, 'empty-component', 'gw', self.public_cloud_id, ['aws_internet_gateway'])
        assert_otm(otm, 1, 'cloudtrail', 'foobar', self.public_cloud_id, ['aws_cloudtrail'])
        assert_otm(otm, 2, 'cognito', 'main', self.public_cloud_id, ['aws_cognito_identity_pool'])
        assert_otm(otm, 3, 'cognito', 'pool', self.public_cloud_id, ['aws_cognito_user_pool'])
        assert_otm(otm, 4, 'elastic-container-service', 'mongo', self.public_cloud_id, ['aws_ecs_service'])
        assert_otm(otm, 5, 'docker-container', 'service', self.public_cloud_id, ['aws_ecs_task_definition'])
        assert_otm(otm, 6, 'docker-container', 'service_task', self.public_cloud_id, ['aws_ecs_task_definition'])
        assert_otm(otm, 7, 'elastic-container-kubernetes', 'example', self.public_cloud_id, ['aws_eks_cluster'])
        assert_otm(otm, 8, 'load-balancer', 'wu-tang', self.public_cloud_id, ['aws_elb'])
        assert_otm(otm, 9, 'load-balancer', 'lb', self.public_cloud_id, ['aws_lb'])
        assert_otm(otm, 10, 'aws-lambda-function', 'test_lambda', self.public_cloud_id, ['aws_lambda_function'])
        assert_otm(otm, 11, 'CD-AWS-NETWORK-FIREWALL', 'firewall_example', self.public_cloud_id,
                   ['aws_networkfirewall_firewall'])
        assert_otm(otm, 12, 'rds', 'mysql', self.public_cloud_id, ['aws_db_instance'])
        assert_otm(otm, 13, 'rds', 'aurora-cluster-demo', self.public_cloud_id, ['aws_rds_cluster'])
        assert_otm(otm, 14, 'redshift', 'tf-redshift-cluster', self.public_cloud_id, ['aws_redshift_cluster'])
        assert_otm(otm, 15, 'route-53', 'route-53-zone-example', self.public_cloud_id, ['aws_route53_zone'])
        assert_otm(otm, 16, 's3', 'foo_s3_bucket', self.public_cloud_id, ['aws_s3_bucket'])
        assert_otm(otm, 17, 'sqs-simple-queue-service', 'terraform_queue', self.public_cloud_id, ['aws_sqs_queue'])
        assert_otm(otm, 18, 'empty-component', 'some-canary', self.public_cloud_id, ['aws_synthetics_canary'])
        assert_otm(otm, 19, 'step-functions', 'my_sfn_activity', self.public_cloud_id, ['aws_sfn_activity'])
        assert_otm(otm, 20, 'step-functions', 'my_sfn_state_machine', self.public_cloud_id, ['aws_sfn_state_machine'])

    def test_aws_parent_children_components(self):
        filename = test_resource_paths.terraform_aws_parent_children_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm(
            'Test case AWS with $parent and $children components',
            'aws_parent_children_components',
            IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-parent-children-terraform.otm', filename)

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.components) == 2
        assert_otm(otm, 0, 'elastic-container-service', 'mongo', self.public_cloud_id, ['aws_ecs_service'])
        assert_otm(otm, 1, 'docker-container', 'service', otm.components[0].id, ['aws_ecs_task_definition'])

    def test_aws_singleton_components(self):
        filename = test_resource_paths.terraform_aws_singleton_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS singleton components', 'aws_singleton_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-singleton-terraform.otm', filename)

        assert iac_to_otm.source_model.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 20
        assert len(otm.dataflows) == 0
        assert_otm(otm, 0, 'CD-ACM', 'acm_certificate', self.public_cloud_id, ['aws_acm_certificate'])
        assert_otm(otm, 1, 'cloudwatch', 'cloudwatch (grouped)', self.public_cloud_id, [
            'cloudwatch_metric_alarm_1 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_metric_alarm_2 (aws_cloudwatch_metric_alarm)',
            'cloudwatch_log_group_1 (aws_cloudwatch_log_group)',
            'cloudwatch_log_group_2 (aws_cloudwatch_log_group)'
        ])
        assert_otm(otm, 2, 'kms', 'kms_key', self.public_cloud_id, ['aws_kms_key'])
        assert_otm(otm, 3, 'CD-SECRETS-MANAGER', 'CD-SECRETS-MANAGER (grouped)', self.public_cloud_id, [
            'secretsmanager_secret_1 (aws_secretsmanager_secret)',
            'secretsmanager_secret_2 (aws_secretsmanager_secret)'
        ])
        assert_otm(otm, 4, 'CD-SYSTEMS-MANAGER', 'CD-SYSTEMS-MANAGER (grouped)', self.public_cloud_id, [
            'ssm_parameter (aws_ssm_parameter)',
            'ssm_document (aws_ssm_document)'
        ])
        assert_otm(otm, 5, 'api-gateway', 'api-gateway (grouped)', self.public_cloud_id, [
            'api_gateway_api_key (aws_api_gateway_api_key)',
            'api_gateway_client_certificate (aws_api_gateway_client_certificate)'
        ])
        assert_otm(otm, 6, 'athena', 'athena (grouped)', self.public_cloud_id, [
            'athena_workgroup (aws_athena_workgroup)',
            'athena_database (aws_athena_database)'
        ])
        assert_otm(otm, 7, 'CD-MQ', 'CD-MQ (grouped)', self.public_cloud_id, [
            'mq_broker (aws_mq_broker)',
            'mq_configuration (aws_mq_configuration)'
        ])
        assert_otm(otm, 8, 'cf-cloudfront', 'cf-cloudfront (grouped)', self.public_cloud_id, [
            'cloudfront_origin_access_identity (aws_cloudfront_origin_access_identity)',
            'cloudfront_public_key (aws_cloudfront_public_key)'
        ])
        assert_otm(otm, 9, 'CD-CONFIG', 'CD-CONFIG (grouped)', self.public_cloud_id, [
            'config_config_rule (aws_config_config_rule)',
            'config_configuration_recorder (aws_config_configuration_recorder)'
        ])
        assert_otm(otm, 10, 'elastic-container-registry', 'elastic-container-registry (grouped)', self.public_cloud_id,
                   [
                       'ecr_repository (aws_ecr_repository)',
                       'ecr_lifecycle_policy (aws_ecr_lifecycle_policy)'
                   ])
        assert_otm(otm, 11, 'elasticache', 'elasticache (grouped)', self.public_cloud_id, [
            'elasticache_user (aws_elasticache_user)',
            'elasticache_user_group (aws_elasticache_user_group)'
        ])
        assert_otm(otm, 12, 'CD-GUARDDUTY', 'CD-GUARDDUTY (grouped)', self.public_cloud_id, [
            'guardduty_detector_1 (aws_guardduty_detector)',
            'guardduty_detector_2 (aws_guardduty_detector)'
        ])
        assert_otm(otm, 13, 'CD-INSPECTOR', 'CD-INSPECTOR (grouped)', self.public_cloud_id, [
            'inspector_resource_group (aws_inspector_resource_group)',
            'inspector_assessment_target (aws_inspector_assessment_target)'
        ])
        assert_otm(otm, 14, 'CD-MACIE', 'CD-MACIE (grouped)', self.public_cloud_id, [
            'macie2_account (aws_macie2_account)',
            'macie2_member (aws_macie2_member)'
        ])
        assert_otm(otm, 15, 'CD-SES', 'CD-SES (grouped)', self.public_cloud_id, [
            'ses_receipt_filter (aws_ses_receipt_filter)',
            'ses_receipt_rule (aws_ses_receipt_rule)'
        ])
        assert_otm(otm, 16, 'sns', 'sns (grouped)', self.public_cloud_id, [
            'sns_topic (aws_sns_topic)',
            'sns_topic_subscription (aws_sns_topic_subscription)'
        ])
        assert_otm(otm, 17, 'CD-WAF', 'CD-WAF (grouped)', self.public_cloud_id, [
            'waf_ipset (aws_waf_ipset)',
            'waf_rule (aws_waf_rule)'
        ])
        assert_otm(otm, 18, 'kinesis-data-analytics', 'kinesis-data-analytics (grouped)', self.public_cloud_id, [
            'kinesis_analytics_application_1 (aws_kinesis_analytics_application)',
            'kinesis_analytics_application_2 (aws_kinesis_analytics_application)',
            'kinesis_stream (aws_kinesis_stream)',
            'kinesis_stream_consumer (aws_kinesis_stream_consumer)'
        ])
        assert_otm(otm, 19, 'kinesis-data-firehose', 'kinesis-data-firehose (grouped)', self.public_cloud_id, [
            'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)',
            'kinesis_firehose_delivery_stream_1 (aws_kinesis_firehose_delivery_stream)'
        ])

    def test_aws_altsource_components(self):
        filename = test_resource_paths.terraform_aws_altsource_components
        mapping_filename = test_resource_paths.default_terraform_aws_mapping
        iac_to_otm = IacToOtm('Test case AWS altsource components', 'aws_altsource_components', IacType.TERRAFORM)
        iac_to_otm.run(IacType.TERRAFORM, mapping_filename, 'threatmodel-from-altsource-terraform.otm', filename)

        assert iac_to_otm.otm
        otm = iac_to_otm.otm
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 12
        assert len(otm.dataflows) == 0
        assert_otm(otm, 0, 'empty-component', 'subnets', self.public_cloud_id, ['aws_subnet'])
        assert_otm(otm, 1, 'empty-component', 'ec2', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 2, 'empty-component', 'ec2_messages', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 3, 'empty-component', 'ssm', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 4, 'empty-component', 'ssm_messages', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 5, 'empty-component', 'ecr', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 6, 'empty-component', 'dynamodb', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 7, 'empty-component', 's3', self.public_cloud_id, ['aws_vpc_endpoint'])
        assert_otm(otm, 8, 's3', 'S3 from VPCEndpoint', self.public_cloud_id, ['s3 (aws_vpc_endpoint)'])
        assert_otm(otm, 9, 'dynamodb', 'DynamoDB from VPCEndpoint', self.public_cloud_id,
                   ['dynamodb (aws_vpc_endpoint)'])
        assert_otm(otm, 10, 'CD-SYSTEMS-MANAGER', 'Systems Manager from VPCEndpoint (grouped)', self.public_cloud_id,
                   [
                       'ssm (aws_vpc_endpoint)',
                       'ssm_messages (aws_vpc_endpoint)'
                   ])
        assert_otm(otm, 11, 'elastic-container-registry', 'ECR from VPCEndpoint', self.public_cloud_id,
                   ['ecr (aws_vpc_endpoint)'])
