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

variables = {
    "whitelist_cidrs": ['255.255.255.0/32', '255.255.255.1/32']
}

INTERNET_CLIENT_ID = 'b0a3f48b-e876-4903-9931-31a1c7e29c17'


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
    @pytest.mark.parametrize('ingress_cidr, mocked_components_in_sgs, expected_id', [
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp'),
            {'SG1': [_component_a]}, INTERNET_CLIENT_ID, id='Ingress HTTP to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTPS', from_port=443, to_port=443, protocol='tcp'),
            {'SG1': [_component_a]}, INTERNET_CLIENT_ID, id='Ingress HTTPS to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0', '255.255.255.255/32'], description='Ingress All', from_port=0, to_port=0, protocol='-1'),
            {'SG1': [_component_a]}, '7bf408da-3c58-4ec4-93a3-aba7665175d0', id='Ingress All to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['255.255.255.255/32', '0.0.0.0/0'], description='Ingress All', from_port=0, to_port=0, protocol='-1'),
            {'SG1': [_component_a]}, '7bf408da-3c58-4ec4-93a3-aba7665175d0', id='Ingress All to component_a'),
    ])
    def test_ingress_dataflows(self,
                               ingress_cidr: SecurityGroupCIDR,
                               mocked_components_in_sgs: Dict[str, List[TFPlanComponent]], expected_id: str):
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
        assert otm.components[1].id == expected_id
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
        pytest.param('172.31.0.0/0', {'SG1': [_component_a]}, id='Private IP address in the "Class B" network range'),
        pytest.param('192.168.0.0/0', {'SG1': [_component_a]}, id='Private IP address in the "Class C" network range'),
        pytest.param('169.254.0.0/0', {'SG1': [_component_a]}, id='Link-local IP address'),
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
        assert otm.dataflows[0].source_node == INTERNET_CLIENT_ID
        assert otm.dataflows[0].destination_node == _component_a.id
        assert otm.dataflows[0].name == 'Ingress HTTP'
        assert not otm.dataflows[0].bidirectional

        # AND it generates a dataflow from the Internet to component_a
        assert otm.dataflows[1].source_node == INTERNET_CLIENT_ID
        assert otm.dataflows[1].destination_node == _component_a.id
        assert otm.dataflows[1].name == 'Ingress HTTPS'
        assert not otm.dataflows[1].bidirectional

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('cidr_blocks, mocked_components_in_sgs, expected_client_id, expected_client_name', [
        pytest.param(
            ['255.255.255.0/32', '255.255.255.1/32'], {'SG1': [_component_a]},
            '2fcb86af-123c-44f8-be57-6d32bb680c80', 'whitelist_cidrs',
            id='exists cidr in whitelist_cidrs'),
        pytest.param(
            ['255.255.255.1/32', '255.255.255.0/32'], {'SG1': [_component_a]},
            '2fcb86af-123c-44f8-be57-6d32bb680c80', 'whitelist_cidrs',
            id='exists cidr in whitelist_cidrs (reverse)'),
        pytest.param(
            ['255.255.255.0/32', '0.0.0.0/0'], {'SG1': [_component_a]},
            '3fac1ad2-e0ba-4a4d-bb35-bb35515c5ce0', 'Ingress HTTP',
            id='not exists cidr in whitelist_cidrs'),
    ])
    def test_security_group_cidr_multiple_ips(self,
                                              cidr_blocks: List[str],
                                              mocked_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                              expected_client_id: str, expected_client_name: str):
        # GIVEN an Ingress HTTP Security Group from a multiple ips to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
            cidr_blocks, description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups, variables=variables)

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

        # AND the client_id and name is the expected
        assert otm.components[1].id == expected_client_id
        assert otm.components[1].name == expected_client_name

        # AND the otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # AND it generates 2 dataflows
        assert len(otm.dataflows) == 1

        # AND it generates a dataflow to component_a
        assert otm.dataflows[0].source_node == expected_client_id
        assert otm.dataflows[0].destination_node == _component_a.id
        assert otm.dataflows[0].name == 'Ingress HTTP'
        assert not otm.dataflows[0].bidirectional

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a]}, id='name is attack surface client type')
    ])
    def test_security_group_without_description_and_multiple_cidrs(self,
                                                                   mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[
            build_security_group_cidr_mock(
                ['255.255.255.0/32', '255.255.255.1/32'], description=None, from_port=80, to_port=80, protocol='tcp')])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_mapping)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the client has the following name
        assert otm.components[1].name == attack_surface_mapping.client

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('ingress_cidr, mocked_components_in_sgs, expected_tags', [
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp'),
            {'SG1': [_component_a]}, ["protocol: tcp", "from_port: 80 to_port: 80", 'ip: 0.0.0.0/0'],
            id='Ingress HTTP to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['0.0.0.0/0', '255.255.255.255/32'], description='Ingress All', from_port=0, to_port=10, protocol='-1'),
            {'SG1': [_component_a]},
            ["protocol: all", "from_port: 0 to_port: 10", "ip: 0.0.0.0/0"],
            id='Ingress All to component_a'),
        pytest.param(build_security_group_cidr_mock(
            ['255.255.255.0/32', '0.0.0.0/0'], description='Ingress All', protocol='-1'),
            {'SG1': [_component_a]},
            ["protocol: all", "from_port: N/A to_port: N/A", "ip: 255.255.255.0/32", "ip: 0.0.0.0/0"],
            id='Ingress All to component_a without defined ports'),
    ])
    def test_generate_security_group_cidr_tags(self,
                                               ingress_cidr: SecurityGroupCIDR,
                                               mocked_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                               expected_tags: List[str]):
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
        for i, tag in enumerate(expected_tags):
            assert otm.dataflows[0].tags[i] == tag

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
