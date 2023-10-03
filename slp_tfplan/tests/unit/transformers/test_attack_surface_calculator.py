from typing import List, Dict
from unittest.mock import MagicMock, Mock

import pytest
from pytest import param

from otm.otm.entity.trustzone import Trustzone
from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroupCIDR, TFPlanComponent
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator, \
    ComponentRelationshipType
from slp_tfplan.slp_tfplan.transformers.attack_surface_calculator import AttackSurfaceCalculator, \
    _generate_client_id, _generate_client_name
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

attack_surface_configuration = MagicMock(
    client='client',
    trustzone=internet_trustzone)

variables = {
    "whitelist_cidrs": ['255.255.255.0/32', '255.255.255.1/32']
}

INTERNET_CLIENT_ID = 'b0a3f48b-e876-4903-9931-31a1c7e29c17'
ALL_ALLOWED_CIDR_BLOCK = '0.0.0.0/0'
ALL_ALLOWED_CIDR_DESCRIPTION = 'All inbound connections allowed'


@pytest.fixture
def mock_components_in_sgs(mocker, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
    if mocked_components_in_sgs is None:
        mocked_components_in_sgs = {}
    mocker.patch.object(ComponentsAndSGsMatcher, 'match', return_value=mocked_components_in_sgs)


@pytest.fixture
def mock_get_variable_name_by_value(mocker, mocked_var_name: str):
    mocker.patch('slp_tfplan.slp_tfplan.transformers.attack_surface_calculator._get_variable_name_by_value',
                 side_effect=[mocked_var_name])


@pytest.fixture
def mock_is_valid_cidr(mocker, mocked_is_valid_cidr: str):
    mocker.patch('slp_tfplan.slp_tfplan.transformers.attack_surface_calculator._is_valid_cidr',
                 side_effect=[mocked_is_valid_cidr])


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


class TestGenerateClientName:
    @pytest.mark.usefixtures('mock_get_variable_name_by_value')
    @pytest.mark.usefixtures('mock_is_valid_cidr')
    @pytest.mark.parametrize('mocked_var_name,mocked_is_valid_cidr,cidr_description,expected_name', [
        pytest.param('var_name', False, None, 'var_name', id='by cidr block variable name'),
        pytest.param(None, True, None, ALL_ALLOWED_CIDR_BLOCK, id='by cidr block'),
        pytest.param(None, False, ALL_ALLOWED_CIDR_DESCRIPTION, ALL_ALLOWED_CIDR_DESCRIPTION, id='by cidr description'),
        pytest.param(None, False, None, INTERNET_CLIENT_ID, id='by default attack surface client')
    ])
    def test_generate_client_name(self,
                                  mocked_var_name, mocked_is_valid_cidr, cidr_description: str, expected_name: str):
        # GIVEN a mocked SecurityGroupCIDR with a list of CIDR blocks
        security_group_cidr = build_security_group_cidr_mock([ALL_ALLOWED_CIDR_BLOCK], cidr_description)

        # AND an attack surface client
        attack_surface_client = INTERNET_CLIENT_ID

        # WHEN AttackSurfaceCalculator::generate_client_name is called
        client_name = _generate_client_name(security_group_cidr, Mock(), attack_surface_client)

        # THEN the Client Name is properly calculated
        assert client_name == expected_name


class TestGenerateClientId:
    @pytest.mark.parametrize('cidr_blocks,expected_id', [
        pytest.param(None, None, id='no cidr blocks'),
        pytest.param([], None, id='empty cidr blocks'),
        pytest.param(['0.0.0.0/0'], 'b0a3f48b-e876-4903-9931-31a1c7e29c17', id='single cidr block'),
        pytest.param(['192.168.0.0/24', '10.0.0.0/16'], '723437a1-1c81-4d1f-b93c-13e06389a5b9',
                     id='multiple cidr block')
    ])
    def test_generate_client_id(self, cidr_blocks: List[str], expected_id: str):
        # GIVEN a mocked SecurityGroupCIDR with a list of CIDR blocks
        security_group_cidr = build_security_group_cidr_mock(cidr_blocks)

        # WHEN AttackSurfaceCalculator::generate_client_name is called
        client_id = _generate_client_id(security_group_cidr)

        # THEN the Client ID is a UUID for a comma-concatenated str of the CIDR blocks
        assert client_id == expected_id


class TestAttackSurfaceCalculator:

    def test_no_attack_surface(self):
        # GIVEN an attack surface with no client
        attack_surface = MagicMock(client=None)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            MagicMock(),
            MagicMock(),
            attack_surface)
        attack_surface_calculator.add_clients_and_dataflows = MagicMock()

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator does not calculate clients and dataflows
        attack_surface_calculator.add_clients_and_dataflows.assert_not_called()

    @pytest.mark.usefixtures('mock_components_in_sgs')
    @pytest.mark.parametrize('mocked_components_in_sgs', [
        pytest.param({'SG1': [_component_a]}, id='SG1 related to component_a'),
    ])
    def test_no_security_group_cidr_info(self,
                                         mock_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                         mocked_components_in_sgs):
        # GIVEN a Security Group without CIDR info
        security_groups = [build_security_group_mock('SG1')]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_configuration)

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
            attack_surface_configuration)

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
        assert otm.components[1].parent == 'internet-trustzone-id'

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
            attack_surface_configuration)

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
            attack_surface_configuration)

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
            attack_surface_configuration)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 2

        # AND the client_id and name is the expected
        assert otm.components[1].id == expected_client_id
        assert otm.components[1].name == expected_client_name

        # AND the parents are the expected
        assert otm.components[1].parent == 'internet-trustzone-id'
        assert otm.components[0].parent == 'default-trustzone-id'

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
    def test_security_group_without_description_and_multiple_cidrs(self, mocked_components_in_sgs: Dict[
        str, List[TFPlanComponent]]):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[
            build_security_group_cidr_mock(
                ['255.255.255.0/32', '255.255.255.1/32'], description=None, from_port=80, to_port=80, protocol='tcp')])]

        otm = build_mocked_otm([_component_a], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_configuration)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the client has the following name
        assert otm.components[1].name == attack_surface_configuration.client

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
            attack_surface_configuration)

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
    def test_remove_parent_dataflows(self,
                                     mock_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                     mocked_components_in_sgs):
        # GIVEN an Ingress HTTP Security Group from Internet to component_a and component_b
        security_groups = [build_security_group_mock('SG1', ingress_cidr=[build_security_group_cidr_mock(
            ['0.0.0.0/0'], description='Ingress HTTP', from_port=80, to_port=80, protocol='tcp')])]

        # AND component_a is parent of component_b
        otm = build_mocked_otm([_component_a, _component_b], security_groups=security_groups)

        # AND an attack surface calculator
        attack_surface_calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_configuration)

        # WHEN the attack surface calculator is transformed
        attack_surface_calculator.transform()

        # THEN the attack surface calculator calculates the dataflows
        # AND the otm has 2 components
        assert len(otm.components) == 3

        # AND the otm has 2 trustzones
        assert len(otm.trustzones) == 2

        # AND it generates 1 dataflow
        assert len(otm.dataflows) == 1

    @pytest.mark.parametrize('parent_id', [
        param('internet-trustzone-id', id='component_with_parent_and_no_previous_tz_internet')
    ])
    def test_add_attack_surface_trustzone_when_needed(self, parent_id):
        # GIVEN an extra component with custom parent id
        generic_client = build_mocked_component({
            'component_name': 'component_k',
            'tf_type': 'generic-client',
            'parent_id': parent_id
        })
        # AND the otm with 3 components
        otm = build_mocked_otm([_component_a, _component_b, generic_client])

        # AND the attack surface calculator
        calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_configuration)
        # WHEN we add the attack surface trust zone
        calculator.add_attack_surface_trustzone()
        # THEN the trust zones are the expected
        assert len(otm.trustzones) == 2
        assert otm.trustzones[0].id == 'default-trustzone-id'
        assert otm.trustzones[0].name == 'default-trustzone-name'
        assert otm.trustzones[0].type == 'default-trustzone-type'
        assert otm.trustzones[1].id == 'internet-trustzone-id'
        assert otm.trustzones[1].name == 'Internet Trustzone'
        assert otm.trustzones[1].type == 'Internet'
        # AND the components are the expected
        assert len(otm.components) == 3
        assert otm.components[0].id == 'aws_type.component_a'
        assert otm.components[0].parent == 'default-trustzone-id'
        assert otm.components[1].id == 'aws_type.component_b'
        assert otm.components[1].parent == 'default-trustzone-id'
        assert otm.components[2].id == 'generic-client.component_k'
        assert otm.components[2].parent == 'internet-trustzone-id'

    @pytest.mark.parametrize('parent_id,extra_trustzone', [
        param('internet-trustzone-id', internet_trustzone, id='component_with_parent_but_previous_tz'),
        param('default-trustzone-id', internet_trustzone, id='no_component_with_parent_and_previous_tz'),
        param('default-trustzone-id', None, id='no_component_with_parent_and_no_previous_tz_1tz'),
        param('default-trustzone-id', Trustzone('99', 'dummy', type='00000'),
              id='no_component_with_parent_and_no_previous_tz_2tz'),
    ])
    def test_add_attack_surface_trustzone_when_not_needed(self, parent_id, extra_trustzone: Trustzone):
        # GIVEN a generic client with internet tz as parent
        generic_client = build_mocked_component({
            'component_name': 'component_k',
            'tf_type': 'generic-client',
            'parent_id': parent_id
        })
        # AND the otm with 3 components
        otm = build_mocked_otm([_component_a, _component_b, generic_client])

        # AND an extra trust zone
        if extra_trustzone:
            otm.trustzones.append(extra_trustzone)

        # AND the attack surface calculator
        calculator = AttackSurfaceCalculator(
            otm,
            MagicMock(),
            attack_surface_configuration)
        # WHEN we add the attack surface trust zone
        calculator.add_attack_surface_trustzone()
        # THEN the trust zones are the expected
        assert len(otm.trustzones) == 2 if extra_trustzone else 1
        assert otm.trustzones[0].id == 'default-trustzone-id'
        assert otm.trustzones[0].name == 'default-trustzone-name'
        assert otm.trustzones[0].type == 'default-trustzone-type'
        if extra_trustzone:
            assert otm.trustzones[1].id == extra_trustzone.id
            assert otm.trustzones[1].name == extra_trustzone.name
            assert otm.trustzones[1].type == extra_trustzone.type
        # AND the components are the expected
        assert len(otm.components) == 3
        assert otm.components[0].id == 'aws_type.component_a'
        assert otm.components[0].parent == 'default-trustzone-id'
        assert otm.components[1].id == 'aws_type.component_b'
        assert otm.components[1].parent == 'default-trustzone-id'
        assert otm.components[2].id == 'generic-client.component_k'
        assert otm.components[2].parent == parent_id
