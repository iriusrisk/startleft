import networkx as nx
import pytest

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.tests.resources.test_resource_paths import aws_ingesting_click_logs


def create_tf_component(component_id: str):
    return TFPlanComponent(component_id, '', '', '', ParentType.TRUST_ZONE, [],
                           tf_resource_id=component_id)


class TestRelationshipsExtractor:

    @pytest.mark.parametrize('source_label, expected', [
        pytest.param('aws_glue_catalog_database.aws_glue_click_logger_database',
                     ['provider["registry.terraform.io/hashicorp/aws"]'],
                     id='UC1'),
        pytest.param('aws_api_gateway_account.click_logger_api_gateway_account',
                     ['aws_iam_role.click_logger_api_gateway_cloudwatch_role'],
                     id='UC2'),
        pytest.param('aws_iam_role_policy_attachment.click_loggerlambda_policy',
                     ['data.aws_iam_policy_document.AWSLambdaTrustPolicy'],
                     id='UC3'),
        pytest.param(
            'aws_lambda_function.lambda_clicklogger_stream_consumer',
            ['provider["registry.terraform.io/hashicorp/aws"]', 'data.aws_iam_policy_document.AWSLambdaTrustPolicy'],
            id='UC4'),
        pytest.param(
            'aws_api_gateway_integration_response.MyDemoIntegrationResponse',
            ['aws_api_gateway_request_validator.clicklogger_validator'],
            id='UC5'),
        pytest.param(
            'aws_cloudwatch_log_group.lambda_click_logger_authorizer_log_group',
            ['data.aws_iam_policy_document.AWSLambdaTrustPolicy'],
            id='UC6'),
        pytest.param(
            'aws_api_gateway_integration.integration',
            ['aws_api_gateway_request_validator.clicklogger_validator'],
            id='UC7')
    ])
    def test_get_shortest_valid_path(self, source_label: str, expected: list):
        # GIVEN a valid Graph
        graph = nx.drawing.nx_agraph.read_dot(aws_ingesting_click_logs)

        # AND the TFPlanComponents
        source: TFPlanComponent = create_tf_component(source_label)
        targets: [TFPlanComponent] = [
            source,
            create_tf_component('aws_api_gateway_request_validator.clicklogger_validator'),
            create_tf_component('aws_iam_role_policy.click_logger_invocation_policy'),
            create_tf_component('aws_iam_role_policy_attachment.lambda_logs'),
            create_tf_component('aws_lambda_permission.apigw_lambda'),
            create_tf_component('provider["registry.terraform.io/hashicorp/aws"]'),
            create_tf_component('aws_iam_role_policy.click_logger_stream_consumer_firehose_inline_policy'),
            create_tf_component('data.aws_iam_policy_document.AWSLambdaTrustPolicy'),
            create_tf_component('aws_glue_catalog_database.aws_glue_click_logger_database'),
            create_tf_component('aws_iam_role.click_logger_api_gateway_cloudwatch_role'),
            create_tf_component('aws_api_gateway_integration_response.MyDemoIntegrationResponse')
        ]

        # AND the extractor
        extractor = RelationshipsExtractor(graph, [])

        # WHEN RelationshipsExtractor::get_closest_resources is invoked
        result = extractor.get_closest_resources(source, targets)

        # THEN the closest resources are the expected ones
        assert result == expected
