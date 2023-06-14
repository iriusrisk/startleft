from typing import List

from networkx import DiGraph
from pytest import mark, param

from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_by_straight_relationship_strategy import \
    DataflowByStraightRelationshipStrategy
from slp_tfplan.tests.util.builders import build_tfgraph, build_simple_mocked_component, build_mocked_otm


def create_relationships_extractor_mock(graph: DiGraph):
    return RelationshipsExtractor(mapped_resources_ids=[], graph=graph)


class TestDataflowByStraightRelationshipStrategy:

    @mark.parametrize('components', [
        param([], id='no_components'),
        param([build_simple_mocked_component('A'), build_simple_mocked_component('B')], id='unrelated_components')
    ])
    def test_no_related_components_no_dataflows(self, components: List[TFPlanComponent]):
        # GIVEN a set of non-related components

        # AND a graph with no relationships between components
        relationships_extractor = create_relationships_extractor_mock(build_tfgraph([]))

        # AND a mocked are_hierarchically_related function which returns no hierarchical relationship
        def are_hierarchically_related(c1, c2): return False

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=components),
            relationships_extractor=relationships_extractor,
            are_hierarchically_related=are_hierarchically_related)

        # THEN no DFs are created in the OTM
        assert not dataflows

    def test_simple_parent_components_no_dataflows(self):
        # GIVEN two components hierarchically related
        parent = build_simple_mocked_component('parent')
        child = build_simple_mocked_component('child', parent=parent.id)

        # AND a graph with a relationship between child and parent
        relationships_extractor = create_relationships_extractor_mock(
            build_tfgraph([(child.tf_resource_id, parent.tf_resource_id)]))

        # AND a mocked are_hierarchically_related function which returns parent-ship between child and parent
        def are_hierarchically_related(c1, c2): return True

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=[parent, child]),
            relationships_extractor=relationships_extractor,
            are_hierarchically_related=are_hierarchically_related)

        # THEN no DFs are created in the OTM
        assert not dataflows

    def test_straight_relationship_dataflow_created(self):
        # GIVEN an OTM with two components A and B
        component_a = build_simple_mocked_component('A')
        component_b = build_simple_mocked_component('B')

        # AND a graph with a relationship between A and B
        relationships_extractor = create_relationships_extractor_mock(
            build_tfgraph([(component_a.tf_resource_id, component_b.tf_resource_id)]))

        # AND a mocked are_hierarchically_related function which returns no hierarchical relationship
        def are_hierarchically_related(c1, c2): return False

        # WHEN DataflowByStraightRelationshipStrategy::create_dataflows is invoked
        dataflows = DataflowByStraightRelationshipStrategy().create_dataflows(
            otm=build_mocked_otm(components=[component_a, component_b]),
            relationships_extractor=relationships_extractor,
            are_hierarchically_related=are_hierarchically_related)

        # THEN one dataflow is created
        assert len(dataflows) == 1
        dataflow = dataflows[0]

        # AND the source is A and the destination is B
        assert dataflow.source_node == 'A'
        assert dataflow.destination_node == 'B'
        assert dataflow.name == 'A to B'
