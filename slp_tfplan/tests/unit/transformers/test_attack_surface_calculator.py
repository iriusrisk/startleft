from typing import List, Dict
from unittest.mock import MagicMock

import pytest

from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroupCIDR, TFPlanComponent
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator, \
    ComponentRelationshipType
from slp_tfplan.slp_tfplan.transformers.attack_surface_calculator import AttackSurfaceCalculator
from slp_tfplan.tests.util.builders import build_mocked_component, build_mocked_otm, build_security_group_cidr_mock, \
    build_security_group_mock

_component_a = build_mocked_component({
    'component_name': 'component_a',
    'tf_type': 'aws_type'
})

_component_b = build_mocked_component({
    'component_name': 'component_b',
    'tf_type': 'aws_type'
})

internet_trustzone = MagicMock(id='internet-trustzone-id', type='Internet')
internet_trustzone.name = 'Internet Trustzone'

attack_surface_mapping = MagicMock(
    client='client',
    trustzone=internet_trustzone)


@pytest.fixture
def mock_components_in_sgs(mocker, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
    if mocked_components_in_sgs is None:
        mocked_components_in_sgs = {}
    mocker.patch.object(ComponentsAndSGsMatcher, 'match', return_value=mocked_components_in_sgs)


@pytest.fixture
def mock_component_relationship_calculator(mocker):
    def get_relationship(component_from: TFPlanComponent, component_to: TFPlanComponent):
        if component_from == component_to:
            return ComponentRelationshipType.SAME
        if component_from == _component_a and component_to == _component_b:
            return ComponentRelationshipType.DESCENDANT
        elif component_from == _component_b and component_to == _component_a:
            return ComponentRelationshipType.ANCESTOR
        return ComponentRelationshipType.UNRELATED

    mocker.patch.object(ComponentRelationshipCalculator, 'get_relationship', side_effect=get_relationship)


class TestAttackSurfaceCalculator:

    def test_no_attack_surface(self):
        # GIVEN an attack surface with no client
        attack_surface = MagicMock(client=None)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            MagicMock(),
            MagicMock(),
            attack_surface)
        attack_surface_calculator.calculate_clients_and_dataflows = MagicMock()

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator does not calculate clients and dataflows
        attack_surface_calculator.calculate_clients_and_dataflows.assert_not_called()

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a]}, id='SG1 related to component_a'),
    ])
    def test_no_security_group_cidr_info(self, mock_components_in_sgs: Dict[str, List[TFPlanComponent]]):

        # GIVEN a Security Group without CIDR info
        security_groups = [build_security_group_mock('SG1')]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN no clients and dataflows are calculated
        assert len(otm.components) == 1
        assert len(otm.dataflows) == 0
        assert len(otm.trustzones) == 1

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('ingress_cidr, mocked_components_in_sgs', [
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp'),
            {'SG1': [_component_a]}, id='Ingress HTTP to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTPS', from_port=443, to_port=443, protocol='tcp'),
            {'SG1': [_component_a]}, id='Ingress HTTPS to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0', '192.168.0.0/22'], description='Ingress All', from_port=0, to_port=0, protocol='-1'),
            {'SG1': [_component_a]}, id='Ingress All to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['172.31.0.0/16', '0.0.0.0/0'], description='Ingress All', from_port=0, to_port=0, protocol='-1'),
            {'SG1': [_component_a]}, id='Ingress All to component_a'),
    ])
    def test_ingress_dataflows(self,
                               ingress_cidr: SecurityGroupCIDR,
                               mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[ingress_cidr])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 2

        # THE first component is component_a in the default trustzone
        assert otm.components[0].id == _component_a.id
        assert otm.components[0].parent == 'default-trustzone-id'

        # THE second component is the 'client' in the Internet trustzone
        assert otm.components[1].id == '0.0.0.0/0'
        assert otm.components[1].type == 'client'
        assert otm.components[1].parent == 'Internet'

        # THE otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # THE first trustzone is the default trustzone
        assert otm.trustzones[0].id == 'default-trustzone-id'

        # THE second trustzone is the Internet trustzone
        assert otm.trustzones[1].id == 'internet-trustzone-id'

        # AND it generates a dataflow from the Internet to component_a
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == otm.components[1].id
        assert otm.dataflows[0].destination_node == otm.components[0].id
        assert otm.dataflows[0].name == ingress_cidr.description
        assert not otm.dataflows[0].bidirectional

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('ingress_cidr_ip, mocked_components_in_sgs', [
        pytest.param('10.0.0.0/0', {'SG1': [_component_a]}, id='Private IP address commonly used in local networks'),
        pytest.param('172.16.0.0/0', {'SG1': [_component_a]}, id='Private IP address in the "Class B" network range'),
        pytest.param('172.31.0.0/0', {'SG1': [_component_a]}, id='Private IP address in the "Class B" network range (2)'),
        pytest.param('192.168.0.0/0', {'SG1': [_component_a]}, id='Private IP address in the "Class C" network range'),
        pytest.param('169.254.0.0/0', {'SG1': [_component_a]}, id='Link-local IP address'),
        pytest.param('var.private_ip', {'SG1': [_component_a]}, id='Private IP address variable'),
        pytest.param('255.255.255.255/32', {'SG1': [_component_a]}, id='Broadcast IP address'),
    ])
    def test_ip_not_allowed(self, ingress_cidr_ip: str, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from a private ip to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
            [ingress_cidr_ip], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator does not calculate the dataflows
        # AND the otm has 1 component
        assert len(otm.components) == 1

        # AND the otm has 1 trustzone
        assert len(otm.trustzones) == 1

        # AND it does not generate a dataflow
        assert len(otm.dataflows) == 0

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a], 'SG2': [_component_a]}, id='to the same component'),
    ])
    def test_multiple_security_group_cidr(self, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        security_groups = [
            # GIVEN an Ingress HTTP Security Group from Internet to component_a
            build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
                ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')]),
            # AND an Ingress HTTPS Security Group from Internet to component_a
            build_security_group_mock('SG2', ingress_cidr=[build_security_group_cidr_mock(
                ['0.0.0.0/0'], description='Ingress HTTPS', from_port=443, to_port=443, protocol='tcp')])
        ]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 2

        # AND the otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # AND it generates 2 dataflows
        assert len(otm.dataflows) == 2

        # AND it generates a dataflow from the Internet to component_a
        assert otm.dataflows[0].source_node == '0.0.0.0/0'
        assert otm.dataflows[0].destination_node == _component_a.id
        assert otm.dataflows[0].name == 'Ingress HTTP'
        assert not otm.dataflows[0].bidirectional

        # AND it generates a dataflow from the Internet to component_a
        assert otm.dataflows[1].source_node == '0.0.0.0/0'
        assert otm.dataflows[1].destination_node == _component_a.id
        assert otm.dataflows[1].name == 'Ingress HTTPS'
        assert not otm.dataflows[1].bidirectional

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a]}, id='with one security group')
    ])
    def test_security_group_cidr_multiple_ips(self, mock_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from a multiple ips to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
            ['7.235.083.057/32', '7.235.083.058/32'],
            description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 3

        # AND the otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # AND it generates 2 dataflows
        assert len(otm.dataflows) == 2

        # AND it generates a dataflow from the '7.235.083.057/32' to component_a
        assert otm.dataflows[0].source_node == '7.235.083.057/32'
        assert otm.dataflows[0].destination_node == _component_a.id
        assert otm.dataflows[0].name == 'Ingress HTTP'
        assert not otm.dataflows[0].bidirectional

        # AND it generates a dataflow from the '7.235.083.058/32' to component_a
        assert otm.dataflows[1].source_node == '7.235.083.058/32'
        assert otm.dataflows[1].destination_node == _component_a.id
        assert otm.dataflows[1].name == 'Ingress HTTP'
        assert not otm.dataflows[1].bidirectional

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('ingress_cidr, mocked_components_in_sgs, expected_tag', [
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp'),
            {'SG1': [_component_a]}, "protocol: tcp, from_port: 80, to_port: 80",
            id='Ingress HTTP to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0', '192.168.0.0/22'], description='Ingress All', from_port=0, to_port=10, protocol='-1'),
            {'SG1': [_component_a]}, "protocol: all, from_port: 0, to_port: 10",
            id='Ingress All to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['172.31.0.0/16', '0.0.0.0/0'], description='Ingress All', protocol='-1'),
            {'SG1': [_component_a]}, "protocol: all, from_port: N/A, to_port: N/A",
            id='Ingress All to component_a without defined ports'),
    ])
    def test_generate_security_group_cidr_tags(self,
                                               ingress_cidr: SecurityGroupCIDR,
                                               mock_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                               expected_tag: str):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[ingress_cidr])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the dataflow has the expected tag
        assert otm.dataflows[0].tags[0] == expected_tag

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.usefixtures('mock_component_relationship_calculator')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a, _component_b]}, id='to the same component'),
    ])
    def test_remove_parent_dataflows(self, mock_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a and component_b
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
                ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')])]

        # AND component_a is parent of component_b

        otm = build_mocked_otm([_component_a, _component_b], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 3

        # AND the otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # AND it generates 1 dataflow
        assert len(otm.dataflows) == 1
