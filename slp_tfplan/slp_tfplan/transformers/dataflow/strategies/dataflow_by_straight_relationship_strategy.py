from typing import List

from otm.otm.entity.dataflow import Dataflow
from sl_util.sl_util.injection import register
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    create_dataflow, DataflowCreationStrategyContainer


@register(DataflowCreationStrategyContainer.strategies)
class DataflowByStraightRelationshipStrategy(DataflowCreationStrategy):
    """
    Strategy to find and create dataflows based straight relationships between resources in the tfgraph.
    It creates dataflows when there is a straight relationship between two components in the tfgraph file.
    One relationship is straight when there is no mapped components in the middle. For example:
    - GIVEN three mapped components C1, C2 and C3.
    - AND one non mapped resource R1.
    - THEN C1 -> C2 or C1 -> R1 -> C2 are valid straight relationships between C1 and C2.
    - AND C1 -> C2 -> C3 is an invalid relationship between C1 and C3.
    Apart from this, no dataflows are created between components with a hierarchical relationship between them.
    """

    def create_dataflows(self, **kwargs) -> List[Dataflow]:
        dataflows = []

        otm = kwargs['otm']
        relationships_extractor = kwargs['relationships_extractor']
        component_relationship_calculator = ComponentRelationshipCalculator(otm)

        for component in otm.components:
            for related_component in otm.components:
                if component == related_component:
                    continue

                if relationships_extractor.exist_valid_path(component.tf_resource_id,
                                                            related_component.tf_resource_id) \
                        and not component_relationship_calculator.are_related(component, related_component):
                    dataflows.append(create_dataflow(component, related_component))

        return dataflows
