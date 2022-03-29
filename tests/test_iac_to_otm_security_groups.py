from startleft.api.controllers.iac.iac_type import IacType
from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


class TestApp:

    def test_run_security_groups_use_case_a_1_with_3_components(self):
        """ Use case A.1 with three components and their Security Groups """

        filename = test_resource_paths.cloudformation_for_security_group_tests_json
        mapping_filename = test_resource_paths.cloudformation_for_security_groups_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run(IacType.CLOUDFORMATION, mapping_filename, 'threatmodel-security-groups.otm', filename)

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 2
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) > 1

        assert list(filter(lambda obj: obj.name == 'ServiceLB', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Canary', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceTaskDefinition', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Service', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0', iac_to_otm.otm.components))

        # Expected final dataflows
        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Canary -> ServiceLB'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Canary -> Service'
                        and "-hub-" not in obj.source_node
                        and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

    def test_run_security_groups_use_case_a_2(self):
        """ Use case A.2: two components in a SG, two components in another SG """

        filename = test_resource_paths.cloudformation_for_security_group_tests_2_json
        mapping_filename = test_resource_paths.cloudformation_for_security_groups_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run(IacType.CLOUDFORMATION, mapping_filename, 'threatmodel-security-groups.otm', filename)

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 2
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) > 1

        assert list(filter(lambda obj: obj.name == 'ServiceLB', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceLB2', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'ServiceTaskDefinition', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Service', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Service2', iac_to_otm.otm.components))

        # Expected final dataflows
        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB2 -> Service'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB -> Service2'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'ServiceLB2 -> Service2'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'ServiceLB -> ServiceLB2'
                        and "-hub-" not in obj.source_node
                        and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'ServiceLB2 -> ServiceLB'
                        and "-hub-" not in obj.source_node
                        and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Service -> Service2'
                        and "-hub-" not in obj.source_node
                        and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

        assert not list(filter(lambda obj: obj.name == 'Service2 -> Service'
                        and "-hub-" not in obj.source_node
                        and "-hub-" not in obj.destination_node, iac_to_otm.otm.dataflows))

    def test_run_security_groups_use_case_b(self):
        """ Use case B: components with their SGs with associated connection rules """
        filename = test_resource_paths.cloudformation_for_security_group_tests_json
        mapping_filename = test_resource_paths.cloudformation_for_security_groups_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run(IacType.CLOUDFORMATION, mapping_filename, 'threatmodel-security-groups.otm', filename)

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 2
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) > 1

        assert list(filter(lambda obj: obj.name == 'VPCssm', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCssmmessages', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'VPCmonitoring', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == '0.0.0.0/0'
                    and obj.type == 'generic-client', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == '255.255.255.255/32'
                    and obj.type == 'generic-client', iac_to_otm.otm.components))

        assert list(filter(lambda obj: obj.name == 'VPCssm -> VPCssmSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmSecurityGroup -> VPCssm'
                                       and "-hub-" not in obj.source_node
                                       and "-hub-" not in obj.destination_node
                           , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmmessages -> VPCssmmessagesSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCssmmessagesSecurityGroup -> VPCssmmessages'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCmonitoring -> VPCmonitoringSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'VPCmonitoringSecurityGroup -> VPCmonitoring'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'Service -> OutboundSecurityGroup'
                    and "-hub-" not in obj.source_node
                    and "-hub-" not in obj.destination_node
                    , iac_to_otm.otm.dataflows))
