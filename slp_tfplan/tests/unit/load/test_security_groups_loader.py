import json
from unittest.mock import MagicMock

from sl_util.sl_util.file_utils import get_byte_data
from slp_tfplan.slp_tfplan.load.security_groups_loader import SecurityGroupsLoader
from slp_tfplan.tests.resources.test_resource_paths import ingress_cidr_from_property, \
    ingress_multiple_cidr_from_property, ingress_multiple_cidr_from_rule, ingress_multiple_security_groups


class TestSecurityGroupsLoader:

    def test_load_ingress_cidr_from_property(self):
        # GIVEN a TFPlanOTM and a TFPlanResources
        tf_plan_resources = json.loads(get_byte_data(ingress_cidr_from_property))
        otm = MagicMock(security_groups=[])

        # WHEN the SecurityGroupsLoader is called
        SecurityGroupsLoader(otm, tf_plan_resources).load()

        # THEN the TFPlanOTM should have the expected SecurityGroups
        assert len(otm.security_groups) == 1
        # AND the SecurityGroup should have the expected CIDR
        assert len(otm.security_groups[0].ingress_cidr) == 1
        assert otm.security_groups[0].ingress_cidr[0].cidr_blocks == ['0.0.0.0/32']
        assert otm.security_groups[0].ingress_cidr[0].description == 'HTTP access to ALB'
        assert otm.security_groups[0].ingress_cidr[0].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[0].from_port == '80'
        assert otm.security_groups[0].ingress_cidr[0].to_port == '80'

    def test_load_multiple_ingress_cidr_from_property(self):
        # GIVEN a TFPlanOTM and a TFPlanResources
        tf_plan_resources = json.loads(get_byte_data(ingress_multiple_cidr_from_property))
        otm = MagicMock(security_groups=[])

        # WHEN the SecurityGroupsLoader is called
        SecurityGroupsLoader(otm, tf_plan_resources).load()

        # THEN the TFPlanOTM should have the expected SecurityGroups
        assert len(otm.security_groups) == 1
        # AND the SecurityGroup should have the expected CIDR
        assert len(otm.security_groups[0].ingress_cidr) == 2
        assert otm.security_groups[0].ingress_cidr[0].cidr_blocks == ['0.0.0.0/32']
        assert otm.security_groups[0].ingress_cidr[0].description == 'HTTP access to ALB'
        assert otm.security_groups[0].ingress_cidr[0].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[0].from_port == '80'
        assert otm.security_groups[0].ingress_cidr[0].to_port == '80'

        assert otm.security_groups[0].ingress_cidr[1].cidr_blocks == ['255.255.255.0/32']
        assert otm.security_groups[0].ingress_cidr[1].description == 'SSH access access to ALB'
        assert otm.security_groups[0].ingress_cidr[1].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[1].from_port == '22'
        assert otm.security_groups[0].ingress_cidr[1].to_port == '22'

    def test_load_multiple_ingress_cidr_from_rule(self):
        # GIVEN a TFPlanOTM and a TFPlanResources
        tf_plan_resources = json.loads(get_byte_data(ingress_multiple_cidr_from_rule))
        otm = MagicMock(security_groups=[])

        # WHEN the SecurityGroupsLoader is called
        SecurityGroupsLoader(otm, tf_plan_resources).load()

        # THEN the TFPlanOTM should have the expected SecurityGroups
        assert len(otm.security_groups) == 1
        # AND the SecurityGroup should have the expected CIDR
        assert len(otm.security_groups[0].ingress_cidr) == 3
        assert otm.security_groups[0].ingress_cidr[0].cidr_blocks == ['255.255.255.0/32', '255.255.255.1/32']
        assert otm.security_groups[0].ingress_cidr[0].description == 'Allows inbound traffic through port 80'
        assert otm.security_groups[0].ingress_cidr[0].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[0].from_port == '80'
        assert otm.security_groups[0].ingress_cidr[0].to_port == '80'

        assert otm.security_groups[0].ingress_cidr[1].cidr_blocks == ['255.255.255.2/32']
        assert otm.security_groups[0].ingress_cidr[1].description == 'Allows inbound traffic through port 443'
        assert otm.security_groups[0].ingress_cidr[1].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[1].from_port == '443'
        assert otm.security_groups[0].ingress_cidr[1].to_port == '443'

        assert otm.security_groups[0].ingress_cidr[2].cidr_blocks == ['0.0.0.0/32']
        assert otm.security_groups[0].ingress_cidr[2].description == 'Allows inbound traffic through port 443'
        assert otm.security_groups[0].ingress_cidr[2].protocol == 'icmp'
        assert otm.security_groups[0].ingress_cidr[2].from_port == '0'
        assert otm.security_groups[0].ingress_cidr[2].to_port == '0'

    def test_load_multiple_security_groups(self):
        # GIVEN a TFPlanOTM and a TFPlanResources
        tf_plan_resources = json.loads(get_byte_data(ingress_multiple_security_groups))
        otm = MagicMock(security_groups=[])

        # WHEN the SecurityGroupsLoader is called
        SecurityGroupsLoader(otm, tf_plan_resources).load()

        # THEN the TFPlanOTM should have the expected SecurityGroups
        assert len(otm.security_groups) == 2
        # AND the SecurityGroup should have the expected CIDR
        assert len(otm.security_groups[0].ingress_cidr) == 1
        assert otm.security_groups[0].ingress_cidr[0].cidr_blocks == ['0.0.0.0/24']
        assert otm.security_groups[0].ingress_cidr[0].description == 'Allows inbound traffic through port 80'
        assert otm.security_groups[0].ingress_cidr[0].protocol == 'tcp'
        assert otm.security_groups[0].ingress_cidr[0].from_port == '80'
        assert otm.security_groups[0].ingress_cidr[0].to_port == '80'

        assert len(otm.security_groups[1].ingress_cidr) == 1
        assert otm.security_groups[1].ingress_cidr[0].cidr_blocks == ['255.255.0.0/32']
        assert otm.security_groups[1].ingress_cidr[0].description == 'HTTP access from ALB'
        assert otm.security_groups[1].ingress_cidr[0].protocol == 'tcp'
        assert otm.security_groups[1].ingress_cidr[0].from_port == '80'
        assert otm.security_groups[1].ingress_cidr[0].to_port == '80'
