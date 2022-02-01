from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


class TestApp:

    def test_run_security_groups_use_case_1(self):
        filename = test_resource_paths.cloudformation_for_security_group_tests_json
        mapping_filename = test_resource_paths.cloudformation_for_security_groups_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run('Cloudformation', mapping_filename, 'threatmodel-security-groups.otm', filename)

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 2
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) > 1

        assert list(filter(lambda obj: obj.name == 'VPCssm', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCssmmessages', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCmonitoring', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', iac_to_otm.otm.components))

        assert list(filter(lambda obj: obj.name == 'VPCssm -> VPCssmSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmmessages -> VPCssmmessagesSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCmonitoring -> VPCmonitoringSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

    def test_run_security_groups_use_case_2(self):
        filename = test_resource_paths.cloudformation_for_security_group_tests_json
        mapping_filename = test_resource_paths.cloudformation_for_security_groups_mapping
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

        # target mappings for the next stage
        # assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service'
        #            and "-hub-" not in obj.source_node
        #            and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        #assert list(filter(lambda obj: obj.name == 'ServiceLB -> OutboundSecurityGroup'
        #            and "-hub-" not in obj.source_node
        #            and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))


