import pytest

from sl_util.sl_util.file_utils import get_data
from slp_base.slp_base.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_base.tests.util.otm import validate_and_diff, validate_and_diff_otm
from slp_cft import CloudformationProcessor
from slp_cft.tests.resources import test_resource_paths
from slp_cft.tests.resources.test_resource_paths import expected_orphan_component_is_not_mapped
from slp_cft.tests.utility import excluded_regex

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_CFT_FILE = test_resource_paths.cloudformation_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.default_cloudformation_mapping
SAMPLE_SINGLE_VALID_CFT_FILE = test_resource_paths.cloudformation_single_file
SAMPLE_VALID_MAPPING_FILE_IR = test_resource_paths.cloudformation_mapping_iriusrisk
SAMPLE_MAPPING_FILE_WITHOUT_REF = test_resource_paths.cloudformation_mapping_without_ref
SAMPLE_NETWORKS_CFT_FILE = test_resource_paths.cloudformation_networks_file
SAMPLE_RESOURCES_CFT_FILE = test_resource_paths.cloudformation_resources_file
SAMPLE_REF_DEFAULT_JSON = test_resource_paths.cloudformation_with_ref_function_and_default_property_json
SAMPLE_REF_DEFAULT_YAML = test_resource_paths.cloudformation_with_ref_function_and_default_property_yaml
SAMPLE_REF_WITHOUT_DEFAULT_JSON = test_resource_paths.cloudformation_with_ref_function_and_without_default_property_json
OTM_EXPECTED_RESULT = test_resource_paths.otm_expected_result
ALTSOURCE_COMPONENTS_OTM_EXPECTED = test_resource_paths.altsource_components_otm_expected


class TestCloudformationProcessor:
    def test_altsource_components(self):
        # GIVEN a valid CFT file with altsource resources
        cft_file = get_data(test_resource_paths.altsource_components_json)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cft_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        assert validate_and_diff(otm, ALTSOURCE_COMPONENTS_OTM_EXPECTED, excluded_regex) == {}

    def test_orphan_component_is_not_mapped(self):
        # GIVEN a valid CFT file with a resource (VPCssm) with a parent which is not declared as component itself (CustomVPC)
        cloudformation_file = get_data(test_resource_paths.cloudformation_orphan_component)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the VPCsmm component without parents is omitted
        # AND the rest of the OTM details match the expected
        assert validate_and_diff(otm.json(), expected_orphan_component_is_not_mapped, excluded_regex) == {}

    def test_component_dataflow_ids(self):
        # GIVEN a valid CFT file with some resources
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_security_group_tests_json)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 22
        assert len(otm.dataflows) == 22

        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service.servicetaskdefinition', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service.servicetaskdefinition', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1.canary', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2.canary', otm.components))
        assert list(filter(lambda obj: obj.id == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.components))
        assert list(filter(lambda obj: obj.id == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup.255_255_255_255_32', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.vpcssm-altsource', otm.components))

        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup.255_255_255_255_32', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup.255_255_255_255_32', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1.canary'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2.canary'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1.canary'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2.canary'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb', otm.dataflows))

    def test_run_valid_mappings(self):
        # GIVEN a valid CFT file with some resources
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_mappings_tests_json)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) > 1
        assert len(otm.dataflows) == 1

        # AND the info inside them is also right
        assert list(filter(lambda obj: obj.name == 'DummyCertificate', otm.components))
        assert list(filter(lambda obj: obj.name == 'RDSCluster', otm.components))
        assert list(filter(lambda obj: obj.name == 'kms (grouped)', otm.components))
        assert list(filter(lambda obj: obj.name == 'sns (grouped)', otm.components))
        assert list(filter(lambda obj: obj.name == 'cloudwatch (grouped)', otm.components))
        assert list(filter(lambda obj: obj.name == 'api-gateway (grouped)', otm.components))
        assert list(filter(lambda obj: obj.name == 'DynamoDB from VPCEndpoint', otm.components))
        assert list(
            filter(lambda obj: obj.name == 'Systems Manager from VPCEndpoint (grouped)', otm.components))
        assert list(
            filter(lambda obj: obj.name == 'API gateway data flow from DummyApiAuthorizer', otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'DummyCertificate'
                                       and "AWS::CertificateManager::Certificate" in obj.tags
                                       and len(obj.tags) == 1, otm.components))
        assert list(filter(lambda obj: obj.name == 'kms (grouped)'
                                       and "DummyTableKey (AWS::KMS::Key)" in obj.tags
                                       and "DummyCanaryBucketKey (AWS::KMS::Key)" in obj.tags
                                       and len(obj.tags) == 2, otm.components))
        assert list(filter(lambda obj: obj.name == 'sns (grouped)'
                                       and "DummySubscription (AWS::SNS::Subscription)" in obj.tags
                                       and "DummyTopic (AWS::SNS::Topic)" in obj.tags
                                       and len(obj.tags) == 2, otm.components))
        assert list(filter(lambda obj: obj.name == 'cloudwatch (grouped)'
                                       and "DummyCWAlarm (AWS::CloudWatch::Alarm)" in obj.tags
                                       and "DummyLogGroupA (AWS::Logs::LogGroup)" in obj.tags
                                       and "DummyLogGroupB (AWS::Logs::LogGroup)" in obj.tags
                                       and len(obj.tags) == 3, otm.components))
        assert list(filter(lambda obj: obj.name == 'api-gateway (grouped)'
                                       and "DummyApiAuthorizer (AWS::ApiGateway::Authorizer)" in obj.tags
                                       and "DummyApiGwKdsRestApi (AWS::ApiGateway::RestApi)" in obj.tags
                                       and len(obj.tags) == 2, otm.components))
        assert list(filter(lambda obj: obj.name == 'Systems Manager from VPCEndpoint (grouped)'
                                       and "DummyVPCssm (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and "DummyVPCssmmessages (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and len(obj.tags) == 2, otm.components))
        assert list(filter(lambda obj: obj.name == "DynamoDB from VPCEndpoint"
                                       and "DummyVPCdynamodb (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and len(obj.tags) == 1, otm.components))

    def test_mapping_component_without_parent(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_component_without_parent)

        # AND an invalid CFT mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.cloudformation_mapping_component_without_parent)

        # WHEN the CFT file is processed
        # THEN an OtmBuildingError is raised
        with pytest.raises(OtmBuildingError) as e_info:
            CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # AND the error references a parent issue
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    def test_mapping_skipped_component_without_parent(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_skipped_component_without_parent)

        # AND a CFT mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.cloudformation_mapping_component_without_parent)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

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

    def test_security_groups_use_case_a_1_with_3_components(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_security_group_tests_json)

        # AND a CFT mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.cloudformation_for_security_groups_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) > 1
        assert len(otm.dataflows) > 1

        # AND the info inside them is also right
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        assert list(filter(lambda obj: obj.name == 'Canary', otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceTaskDefinition', otm.components))
        assert list(filter(lambda obj: obj.name == 'Service', otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))

        # AND the dataflows for SG are generated
        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Canary -> ServiceLB'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Canary -> Service'
                                           and "-hub-" not in obj.source_node
                                           and "-hub-" not in obj.destination_node, otm.dataflows))

    def test_run_security_groups_use_case_a_2(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_security_group_tests_2_json)

        # AND a CFT mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.cloudformation_for_security_groups_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) > 1
        assert len(otm.dataflows) > 1

        # AND the info inside them is also right
        assert list(filter(lambda obj: obj.name == 'ServiceLB', otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceLB2', otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceTaskDefinition', otm.components))
        assert list(filter(lambda obj: obj.name == 'Service', otm.components))
        assert list(filter(lambda obj: obj.name == 'Service2', otm.components))

        # AND the dataflows for SG are generated
        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB2 -> Service'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service2'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB2 -> Service2'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node, otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'ServiceLB -> ServiceLB2'
                                           and "-hub-" not in obj.source_node
                                           and "-hub-" not in obj.destination_node, otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'ServiceLB2 -> ServiceLB'
                                           and "-hub-" not in obj.source_node
                                           and "-hub-" not in obj.destination_node, otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Service -> Service2'
                                           and "-hub-" not in obj.source_node
                                           and "-hub-" not in obj.destination_node, otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Service2 -> Service'
                                           and "-hub-" not in obj.source_node
                                           and "-hub-" not in obj.destination_node, otm.dataflows))

    def test_run_security_groups_use_case_b(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_security_group_tests_json)

        # AND a CFT mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.cloudformation_for_security_groups_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) > 1
        assert len(otm.dataflows) > 1

        # AND the info inside them is also right
        assert list(filter(lambda obj: obj.name == 'VPCssm', otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCssmmessages', otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCmonitoring', otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0'
                                       and obj.type == 'generic-client', otm.components))
        assert list(filter(lambda obj: obj.name == '255.255.255.255/32'
                                       and obj.type == 'generic-client', otm.components))

        # AND the dataflows for SG are generated
        assert list(filter(lambda obj: obj.name == 'VPCssm -> VPCssmSecurityGroup'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmSecurityGroup -> VPCssm'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmmessages -> VPCssmmessagesSecurityGroup'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmmessagesSecurityGroup -> VPCssmmessages'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCmonitoring -> VPCmonitoringSecurityGroup'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCmonitoringSecurityGroup -> VPCmonitoring'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Service -> OutboundSecurityGroup'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , otm.dataflows))

    @pytest.mark.parametrize('mapping_file', [None, [None]])
    def test_mapping_files_not_provided(self, mapping_file):
        # GIVEN a sample valid IaC file (and none mapping file)
        cloudformation_file = [get_data(SAMPLE_VALID_CFT_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises TypeError
        with pytest.raises(TypeError):
            CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [get_data(mapping_file)]).process()

    def test_invalid_mapping_files(self):
        # GIVEN a sample valid IaC file
        cloudformation_file = get_data(SAMPLE_VALID_CFT_FILE)

        # AND an invalid iac mappings file
        mapping_file = [get_data(test_resource_paths.invalid_yaml)]

        # WHEN creating OTM project from IaC file
        # THEN raises MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError):
            CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], mapping_file).process()

    @pytest.mark.parametrize('cloudformation_file',
                             [[get_data(test_resource_paths.cloudformation_invalid_size)],
                              [get_data(test_resource_paths.cloudformation_invalid_size),
                               get_data(test_resource_paths.cloudformation_invalid_size)],
                              [get_data(test_resource_paths.cloudformation_invalid_size),
                               get_data(test_resource_paths.cloudformation_resources_file)]])
    def test_invalid_cloudformation_file(self, cloudformation_file):
        # GIVEN a sample invalid CFT file
        # AND a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises OtmBuildingError
        with pytest.raises(IacFileNotValidError):
            CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, cloudformation_file, mapping_file).process()

    def test_run_valid_simple_iac_mapping_file(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(SAMPLE_SINGLE_VALID_CFT_FILE)
        # AND a valid mapping file
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)

        # WHEN the method CloudformationProcessor::process is invoked
        otm = CloudformationProcessor('multiple-files', 'multiple-files', [cloudformation_file],
                                      [mapping_file]).process()

        # THEN a file with the expected otm is returned
        assert validate_and_diff_otm(otm.json(), OTM_EXPECTED_RESULT, excluded_regex) == {}

    def test_run_valid_multiple_iac_mapping_files(self):
        # GIVEN the valid CFT file
        networks_cft_file = get_data(SAMPLE_NETWORKS_CFT_FILE)
        # AND another valid CFT file
        resources_cft_file = get_data(SAMPLE_RESOURCES_CFT_FILE)
        # AND a valid mapping file
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)
        # WHEN the method CloudformationProcessor::process is invoked
        otm = CloudformationProcessor('multiple-files', 'multiple-files', [networks_cft_file, resources_cft_file],
                                      [mapping_file]).process()
        # THEN a file with the expected otm is returned
        assert validate_and_diff_otm(otm.json(), OTM_EXPECTED_RESULT, excluded_regex) == {}

    def test_run_empty_multiple_iac_files(self):
        # GIVEN a request without any iac_file key
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)
        # WHEN the method CloudformationProcessor::process is invoked
        # THEN an RequestValidationError is raised
        with pytest.raises(LoadingIacFileError):
            CloudformationProcessor('multiple-files', 'multiple-files', [], mapping_file).process()

    @pytest.mark.parametrize('source', [
        # GIVEN a standalone SecurityGroupEgress configuration
        [get_data(test_resource_paths.standalone_securitygroupegress_configuration)],
        # GIVEN a standalone SecurityGroupIngress configuration
        [get_data(test_resource_paths.standalone_securitygroupingress_configuration)]])
    def test_security_group_configuration(self, source):
        # AND a CFT mapping file
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE)
        # WHEN the method CloudformationProcessor::process is invoked
        otm = CloudformationProcessor('id', 'name', source, [mapping_file]).process()
        # THEN otm has a generic-client in Internet Trustzone
        assert otm.components[0].parent_type == 'trustZone'
        assert len(otm.components) == 1
        assert otm.components[0].parent == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'

    def test_multiple_stack_plus_s3_ec2(self):
        # GIVEN the file with multiple Subnet AWS::EC2::Instance different configurations
        cloudformation_file = get_data(test_resource_paths.multiple_stack_plus_s3_ec2)
        # AND a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # WHEN processing
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], mapping_file).process()

        assert len(otm.components) == 9
        publicSubnet1Id = [component for component in otm.components if component.name == 'PublicSubnet1'][0].id
        assert publicSubnet1Id
        ec2WithWrongParent = [component for component in otm.components if
                              component.type == 'ec2' and component.parent != publicSubnet1Id]
        assert len(ec2WithWrongParent) == 0

    def test_parsing_cft_json_file_with_ref(self):
        # GIVEN a cloudformation JSON  file
        cloudformation_file = get_data(SAMPLE_REF_DEFAULT_JSON)
        # AND a mapping file that matches a component whose name is a Ref Value
        # AND the ref value is a Parameter with Default Attribute
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)
        # WHEN parsing the file
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file],
                                      [mapping_file]).process()
        # THEN the component name is the Default attribute of the parameter
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))

    def test_parsing_cft_yaml_file_with_ref(self):
        # GIVEN a cloudformation YAML  file
        cloudformation_file = get_data(SAMPLE_REF_DEFAULT_YAML)
        # AND a mapping file that matches a component whose name is a Ref Value
        # AND the ref value is a Resource
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)
        # WHEN parsing the file
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file],
                                      [mapping_file]).process()
        # THEN the component name is the name of the Resource
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))

    def test_parsing_cft_json_file_without_ref(self):
        # GIVEN a cloudformation file
        cloudformation_file = get_data(SAMPLE_REF_WITHOUT_DEFAULT_JSON)
        # AND a mapping file that matches a component whose name is a Ref Value
        # AND the ref value is a Parameter without Default Attribute
        mapping_file = get_data(SAMPLE_VALID_MAPPING_FILE_IR)
        # WHEN parsing the file
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file],
                                      [mapping_file]).process()
        # THEN the component name is the name of the Parameter
        assert list(filter(lambda obj: obj.name == 'PublicSGSource', otm.components))

    def test_mapping_without_ref_attribute(self):
        # GIVEN a mapping file with searchPath: ["Properties.SubnetId.Ref","Properties.SubnetId"] function
        cloudformation_file = get_data(test_resource_paths.multiple_stack_plus_s3_ec2)
        mapping_file = get_data(SAMPLE_MAPPING_FILE_WITHOUT_REF)
        # WHEN parsing a CFT
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file],
                                      [mapping_file]).process()
        # THEN check if the line could be change for only access to Properties.SubnetId.
        my_ec2_instance2 =  list(filter(lambda obj: obj.name == 'MyEC2Instance2', otm.components))
        public_subnet = list(filter(lambda obj: obj.name == 'PublicSubnet1', otm.components))
        assert my_ec2_instance2[0].parent_type == 'component'
        assert my_ec2_instance2[0].parent == public_subnet[0].id

    def test_minimal_cft_file(self):
        # Given a minimal valid CFT file
        cft_minimal_file = get_data(test_resource_paths.cloudformation_minimal_content)

        # and the default mapping file for CFT
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # When parsing the file with Startleft and the default mapping file
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cft_minimal_file], [mapping_file]).process()

        # Then an empty OTM containing only the default trustzone is generated
        assert validate_and_diff_otm(otm.json(), test_resource_paths.otm_with_only_default_trustzone_expected_result,
                                     excluded_regex) == {}

    def test_generate_empty_otm_with_empty_mapping_file(self):
        # Given an empty mapping file
        mapping_file = get_data(test_resource_paths.empty_cloudformation_mapping)

        # and a valid CFT file with content
        cloudformation_file = get_data(test_resource_paths.cloudformation_for_mappings_tests_json)

        # When parsing the file with Startleft and the empty mapping file
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # Then an empty OTM, without any threat modeling content, is generated
        assert validate_and_diff_otm(otm.json(), test_resource_paths.minimal_otm_expected_result,
                                     excluded_regex) == {}

    def test_security_group_components_from_same_resource(self):
        # GIVEN a valid CFT file with a security group containing both an inbound and an outbound rule
        cloudformation_file = get_data(test_resource_paths.cloudformation_components_from_same_resource)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        #AND the component IDs are differentiated by their IPs
        ingress_id = list(filter(lambda obj: obj.name == '52.30.97.44/32', otm.components))[0].id
        egress_id = list(filter(lambda obj: obj.name == '0.0.0.0/0', otm.components))[0].id

        assert ingress_id != egress_id
        assert '52_30_97_44_32' in ingress_id
        assert '0_0_0_0_0' in egress_id


    def test_trustzone_types(self):
        # GIVEN a valid CFT file
        cloudformation_file = get_data(test_resource_paths.cloudformation_minimal_content)

        # AND a valid CFT mapping file that defines two TZs, one with type and the one without type
        mapping_file = get_data(test_resource_paths.cloudformation_trustzone_types_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

        # AND the trustzone with a defined type has the correct value
        assert list(filter(lambda obj: obj.id == 'public-cloud-01'
                                       and obj.type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91', otm.trustzones))

        # AND the trustzone without a defined type uses the ID value as type
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
                                       and obj.type == obj.id, otm.trustzones))

    def test_components_with_trustzones_of_same_type(self):
        # GIVEN a valid CFT file WITH some components mapped to different TZs of the same type
        cloudformation_file = get_data(test_resource_paths.cloudformation_components_with_trustzones_of_same_type)

        # AND a valid CFT mapping file that defines two different TZs of the same type
        mapping_file = get_data(test_resource_paths.cloudformation_multiple_trustzones_same_type_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        # AND both trustzones have the same type, but different ID
        trustzone1 = list(filter(lambda obj: obj.id == 'public-cloud-01'
                                             and obj.type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91', otm.trustzones))
        trustzone2 = list(filter(lambda obj: obj.id == 'public-cloud-02'
                                             and obj.type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91', otm.trustzones))
        assert trustzone1[0].type == trustzone2[0].type

        # AND each component has the correct trustzone
        assert otm.components[0].parent_type == 'trustZone'
        assert otm.components[0].parent == 'public-cloud-01'
        assert otm.components[1].parent_type == 'trustZone'
        assert otm.components[1].parent == 'public-cloud-02'
