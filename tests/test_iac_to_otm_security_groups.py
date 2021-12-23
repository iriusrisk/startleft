from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


class TestApp:

    def test_run_security_groups_use_case_1(self):
        filename = test_resource_paths.cloudformation_for_security_group_tests_json
        #TODO: change to default mapping before push
        #mapping_filename = test_resource_paths.default_mapping
        mapping_filename = test_resource_paths.TEMP_security_groups_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run('Cloudformation', mapping_filename, 'threatmodel-security-groups.otm', filename)

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 2
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) > 1

        assert list(filter(lambda obj: obj.name == 'ServiceLB', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceTaskDefinition', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Service', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Canary', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', iac_to_otm.otm.components))

        assert list(filter(lambda obj: obj.name == 'Security group dataflow found in Service'
                           and "-hub-" not in obj.source_node
                           and "destination-hub-OutboundSecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Security group dataflow found in ServiceLB'
                                       and "-hub-" not in obj.source_node
                                       and "destination-hub-ServiceLBSecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Security group dataflow found in Canary'
                                       and "-hub-" not in obj.source_node
                                       and "destination-hub-CanarySecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name ==
                                       'Outer Security Group Ingress dataflow found in OutboundSecurityGroupIngressfromServiceLBSecurityGroup'
                                       and "destination-hub-ServiceLBSecurityGroup" in obj.source_node
                                       and "destination-hub-OutboundSecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name ==
                                       'Outer Security Group Egress dataflow found in ServiceLBSecurityGroupEgresstoOutboundSecurityGroup'
                                       and "destination-hub-ServiceLBSecurityGroup" in obj.source_node
                                       and "destination-hub-OutboundSecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name ==
                                       'Outer Security Group Ingress dataflow found in ServiceLBSecurityGroupIngressfromCanarySecurityGroup'
                                       and "destination-hub-CanarySecurityGroup" in obj.source_node
                                       and "destination-hub-ServiceLBSecurityGroup" in obj.destination_node
                           , iac_to_otm.otm.dataflows))