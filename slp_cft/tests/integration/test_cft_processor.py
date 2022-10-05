import pytest

from sl_util.sl_util.file_utils import get_data
from slp_base.slp_base.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError
from slp_cft import CloudformationProcessor
from slp_cft.tests.resources import test_resource_paths

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_CFT_FILE = test_resource_paths.cloudformation_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.default_cloudformation_mapping


class TestCloudformationProcessor:

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
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm-altsource', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm-altsource', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages-altsource', otm.components))
        assert list(filter(lambda obj: obj.id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages-altsource', otm.components))
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
        assert list(filter(lambda obj: obj.id == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.components))
        assert list(filter(lambda obj: obj.id == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup', otm.components))

        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm-altsource', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm-altsource'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm-altsource', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm-altsource'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages-altsource', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages-altsource'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages-altsource', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages-altsource'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
                                       and obj.destination_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup', otm.dataflows))
        assert list(filter(lambda obj: obj.source_node == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service'
                                       and obj.destination_node == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup', otm.dataflows))
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

    @pytest.mark.parametrize('cloudformation_file', [get_data(test_resource_paths.cloudformation_invalid_size)])
    def test_invalid_cloudformation_file(self, cloudformation_file):
        # GIVEN a sample invalid CFT file
        # AND a valid iac mappings file
        mapping_file = [get_data(SAMPLE_VALID_MAPPING_FILE)]

        # WHEN creating OTM project from IaC file
        # THEN raises OtmBuildingError
        with pytest.raises(IacFileNotValidError):
            CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], mapping_file).process()

