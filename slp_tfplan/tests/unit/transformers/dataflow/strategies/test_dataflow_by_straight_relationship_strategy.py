from typing import List

from _pytest.fixtures import fixture
from networkx import DiGraph
from pytest import mark, param

from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_by_straight_relationship_strategy import \
    DataflowByStraightRelationshipStrategy
from slp_tfplan.tests.util.builders import build_tfgraph, build_simple_mocked_component, build_mocked_otm


def create_relationships_extractor_mock(graph: DiGraph):
    return RelationshipsExtractor(mapped_resources_ids=[], graph=graph)


@fixture(autouse=True)
def mock_components_relationship_calculator(mocker, mocked_are_components_related: bool):
    if mocked_are_components_related is None:
        mocked_are_components_related = False
    mocker.patch.object(ComponentRelationshipCalculator, 'are_related', return_value=mocked_are_components_related)


class TestDataflowByStraightRelationshipStrategy:

    @mark.parametrize('components, mocked_are_components_related', [
        param([], False, id='no_components'),
        param([build_simple_mocked_component('A'), build_simple_mocked_component('B')], False,
              id='unrelated_components')
    ])
    def test_no_related_components_no_dataflows(self, components: List[TFPlanComponent],
                                                mocked_are_components_related: bool):
        # GIVEN a set of non-related components

        # AND a graph with no relationships between components
        relationships_extractor = create_relationships_extractor_mock(build_tfgraph([]))

        # AND a mocked are_components_related which returns no hierarchical relationship

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=components),
            relationships_extractor=relationships_extractor)

        # THEN no DFs are created in the OTM
        assert not dataflows

    @mark.parametrize('mocked_are_components_related', [
        param(True, id='components are hierarchically related')
    ])
    def test_simple_parent_components_no_dataflows(self, mocked_are_components_related: bool):
        # GIVEN two components hierarchically related
        parent = build_simple_mocked_component('parent')
        child = build_simple_mocked_component('child', parent=parent.id)

        # AND a graph with a relationship between child and parent
        relationships_extractor = create_relationships_extractor_mock(
            build_tfgraph([(child.tf_resource_id, parent.tf_resource_id)]))

        # AND a mocked are_components_related which returns parent-ship between child and parent

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=[parent, child]),
            relationships_extractor=relationships_extractor)

        # THEN no DFs are created in the OTM
        assert not dataflows

    @mark.parametrize('mocked_are_components_related', [
        param(False, id='components are not hierarchically related')
    ])
    def test_straight_relationship_dataflow_created(self, mocked_are_components_related: bool):
        # GIVEN an OTM with two components A and B
        component_a = build_simple_mocked_component('A')
        component_b = build_simple_mocked_component('B')

        # AND a graph with a relationship between A and B
        relationships_extractor = create_relationships_extractor_mock(
            build_tfgraph([(component_a.tf_resource_id, component_b.tf_resource_id)]))

        # AND a mocked are_components_related which returns no hierarchical relationship

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=[component_a, component_b]),
            relationships_extractor=relationships_extractor)

        # THEN one dataflow is created
        assert len(dataflows) == 1
        dataflow = dataflows[0]

        # AND the source is A and the destination is B
        assert dataflow.source_node == 'A'
        assert dataflow.destination_node == 'B'
        assert dataflow.name == 'A to B'
