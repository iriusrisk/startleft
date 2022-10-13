import pytest

from sl_util.sl_util.file_utils import get_data
from slp_base.slp_base.errors import OtmBuildingError, MappingFileNotValidError, IacFileNotValidError, \
    LoadingIacFileError
from slp_base.tests.util.otm import validate_and_diff_otm
from slp_cft import CloudformationProcessor
from slp_cft.tests.resources import test_resource_paths
from slp_cft.tests.utility import excluded_regex

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
DEFAULT_TRUSTZONE_ID = "b61d6911-338d-46a8-9f39-8dcd24abfe91"
SAMPLE_UNKNOWN_PARENT_CFT_FILE = test_resource_paths.cloudformation_component_with_unknown_parent
SAMPLE_VALID_CFT_FILE = test_resource_paths.cloudformation_for_mappings_tests_json
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.default_cloudformation_mapping
SAMPLE_SINGLE_VALID_CFT_FILE = test_resource_paths.cloudformation_single_file
SAMPLE_VALID_MAPPING_FILE_IR = test_resource_paths.cloudformation_mapping_iriusrisk
SAMPLE_NETWORKS_CFT_FILE = test_resource_paths.cloudformation_networks_file
SAMPLE_RESOURCES_CFT_FILE = test_resource_paths.cloudformation_resources_file
OTM_EXPECTED_RESULT = test_resource_paths.otm_expected_result


class TestCloudformationProcessor:
    def test_set_default_trustzone_as_parent_when_parent_not_exists(self):
        # GIVEN a valid CFT file with a resource (VPCssm) with a parent which is not declared as component itself (CustomVPC)
        cloudformation_file = get_data(test_resource_paths.cloudformation_component_with_unknown_parent)

        # AND a valid CFT mapping file
        mapping_file = get_data(test_resource_paths.default_cloudformation_mapping)

        # WHEN the CFT file is processed
        otm = CloudformationProcessor(SAMPLE_ID, SAMPLE_NAME, [cloudformation_file], [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 1
        assert len(otm.components) == 5

        # AND the VPCssm component has the default trustzone id as parent, instead of the CustomVPC unknown component id
        assert list(filter(lambda component: component.parent_type == 'trustZone' and
                                             component.parent == DEFAULT_TRUSTZONE_ID, otm.components))

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
