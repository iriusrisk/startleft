from typing import List, Callable, Dict
from unittest.mock import Mock, MagicMock

from _pytest.fixtures import fixture
from pytest import mark, param

from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher, SGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_by_security_groups_strategy import \
    DataflowBySecurityGroupsStrategy
from slp_tfplan.tests.util.builders import build_simple_mocked_component


def build_mocked_matcher(are_related: Callable) -> Mock:
    mock = Mock()
    mock.are_related = are_related
    return mock


@fixture(autouse=True)
def mock_components_in_sgs(mocker, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]]):
    if mocked_components_in_sgs is None:
        mocked_components_in_sgs = {}
    mocker.patch.object(ComponentsAndSGsMatcher, 'match', return_value=mocked_components_in_sgs)


@fixture(autouse=True)
def mock_sg_in_sgs(mocker, mocked_sg_in_sgs: Dict[str, List[str]]):
    if mocked_sg_in_sgs is None:
        mocked_sg_in_sgs = []
    mocker.patch.object(SGsMatcher, 'match', return_value=mocked_sg_in_sgs)


@fixture(autouse=True)
def mock_components_relationship_calculator(mocker, mocked_are_components_related: bool):
    if mocked_are_components_related is None:
        mocked_are_components_related = False
    mocker.patch.object(ComponentRelationshipCalculator, 'are_related', return_value=mocked_are_components_related)


tf_plan_component_a = build_simple_mocked_component('A')
tf_plan_component_b = build_simple_mocked_component('B')


class TestDataflowBySecurityGroupsStrategy:

    @mark.parametrize('mocked_components_in_sgs,mocked_sg_in_sgs, mocked_are_components_related', [
        param({}, {}, False, id='no components in security groups'),
        param({'SG1': [tf_plan_component_a]}, {}, False, id='no sg in security groups'),
        param({'SG1': [tf_plan_component_a]}, {'SG2': ['SG3']}, False, id='unrelated_components and SGs'),
    ])
    def test_no_related_components_no_dataflows(self, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                                mocked_sg_in_sgs: Dict[str, List[str]],
                                                mocked_are_components_related: bool):
        # GIVEN a set of unrelated components and security groups

        # WHEN DataflowBySecurityGroupsStrategy::create_dataflows is invoked
        dataflows = DataflowBySecurityGroupsStrategy().create_dataflows(otm=MagicMock())

        # THEN no DFs are created in the OTM
        assert not dataflows

    @mark.parametrize('mocked_components_in_sgs,mocked_sg_in_sgs,mocked_are_components_related,'
                      'expected_source,expected_destination,bidirectional', [
                          param({'SG1': [tf_plan_component_a], 'SG2': [tf_plan_component_b]}, {'SG1': ['SG2']}, False,
                                'A', 'B', False, id='SG1 to SG2'),
                          param({'SG1': [tf_plan_component_a], 'SG2': [tf_plan_component_b]}, {'SG2': ['SG1']}, False,
                                'B', 'A', False, id='SG2 to SG1')
                      ])
    def test_two_related_sgs(self, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]],
                             mocked_sg_in_sgs: Dict[str, List[str]], mocked_are_components_related: bool,
                             expected_source: str, expected_destination: str, bidirectional: bool):
        # GIVEN a set of related components and security groups

        # AND components are not related

        # WHEN DataflowBySecurityGroupsStrategy::create_dataflows is invoked
        dataflows = DataflowBySecurityGroupsStrategy().create_dataflows(otm=MagicMock())

        # THEN one dataflow is created
        assert len(dataflows) == 1
        dataflow = dataflows[0]

        # AND the source and destination are right
        assert dataflow.source_node == expected_source
        assert dataflow.destination_node == expected_destination
        assert dataflow.bidirectional == bidirectional

    @mark.parametrize('mocked_components_in_sgs,mocked_sg_in_sgs,mocked_are_components_related,'
                      'expected_source,expected_destination,bidirectional', [
                          param({'SG1': [tf_plan_component_a], 'SG2': [tf_plan_component_b]}, {'SG1': ['SG2']}, True,
                                'A', 'B', False, id='SG1 to SG2'),
                          param({'SG1': [tf_plan_component_a], 'SG2': [tf_plan_component_b]}, {'SG2': ['SG1']}, True,
                                'B', 'A', False, id='SG2 to SG1')
                      ])
    def test_are_componentes_related(self, mocked_components_in_sgs: Dict[str, List[TFPlanComponent]],
                                        mocked_sg_in_sgs: Dict[str, List[str]], mocked_are_components_related: bool,
                                        expected_source: str, expected_destination: str, bidirectional: bool):
        # GIVEN a set of related components and security groups

        # AND components are related

        # WHEN DataflowBySecurityGroupsStrategy::create_dataflows is invoked
        dataflows = DataflowBySecurityGroupsStrategy().create_dataflows(otm=MagicMock())

        # THEN one dataflow is created
        assert not dataflows
