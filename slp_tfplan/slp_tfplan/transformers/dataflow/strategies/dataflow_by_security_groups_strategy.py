from typing import List

from otm.otm.entity.dataflow import Dataflow
from sl_util.sl_util.injection import register
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.components_and_sgs_matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.matcher.sgs_matcher import SGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    create_dataflow, DataflowCreationStrategyContainer



@register(DataflowCreationStrategyContainer.strategies)
class DataflowBySecurityGroupsStrategy(DataflowCreationStrategy):
    """
    Strategy to find and create dataflows based on AWS Security Groups.
    It creates dataflows for components belonging to related dataflows, for example:
    - GIVEN two Security groups, SG1 and SG2 related in some way (using `MatchStrategy`s).
    - AND two components C1 and C2 belonging to SG1 (using `MatchStrategy`s).
    - AND two components C3 and C4 belonging to SG2 (using `MatchStrategy`s).
    - THEN the DataflowBySecurityGroupsStrategy returns two dataflows: C1 -> C2 and C3 -> C4.
    """

    def __init__(self):
        # Data structures

        self.otm: TFPlanOTM
        self.relationships_extractor: RelationshipsExtractor

        # Injected dependencies
        self.component_relationship_calculator: ComponentRelationshipCalculator

    def create_dataflows(self, **kwargs) -> List[Dataflow]:
        self.otm = kwargs['otm']
        self.relationships_extractor = kwargs.get('relationships_extractor', None)
        self.component_relationship_calculator = ComponentRelationshipCalculator(self.otm)

        return self.__create_dataflows_by_security_groups()

    def __create_dataflows_by_security_groups(self):
        dataflows = []
        components_in_sgs = ComponentsAndSGsMatcher(self.otm, self.relationships_extractor).match()
        if not components_in_sgs:
            return dataflows

        sg_in_sgs = SGsMatcher(self.otm, self.relationships_extractor).match()
        for source_sg, target_sgs in sg_in_sgs.items():
            if source_sg not in components_in_sgs:
                continue

            for target_sg in target_sgs:
                if target_sg in components_in_sgs:
                    dataflows.extend(
                        self.__create_dataflows_among_components(components_in_sgs[source_sg],
                                                                 components_in_sgs[target_sg]))

        return dataflows

    def __create_dataflows_among_components(self,
                                            source_components: List[TFPlanComponent],
                                            target_components: List[TFPlanComponent]):
        dataflows = []

        for source_component in source_components:
            for target_component in target_components:
                if not self.component_relationship_calculator.are_related(source_component, target_component):
                    dataflows.append(create_dataflow(source_component, target_component))

        return dataflows
