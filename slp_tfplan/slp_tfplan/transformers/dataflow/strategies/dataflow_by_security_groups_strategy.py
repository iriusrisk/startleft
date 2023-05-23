from typing import List, Dict, Callable

from dependency_injector.wiring import Provide, inject

from otm.otm.entity.dataflow import Dataflow
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourcesMatcher, ResourcesMatcherContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    create_dataflow, DataflowCreationStrategyContainer
from slp_tfplan.slp_tfplan.util.injection import register


@register(DataflowCreationStrategyContainer.strategies)
class DataflowBySecurityGroupsStrategy(DataflowCreationStrategy):
    @inject
    def __init__(self,
                 sgs_matcher: ResourcesMatcher = Provide[ResourcesMatcherContainer.sgs_resources_matcher],
                 components_sg_matcher: ResourcesMatcher = Provide[ResourcesMatcherContainer.component_sg_matcher]):
        # Data structures

        self.otm: TFPlanOTM
        self.relationships_extractor: RelationshipsExtractor

        # Injected dependencies
        self.are_hierarchically_related: Callable
        self.are_sgs_related = sgs_matcher.are_related
        self.are_component_in_sg = components_sg_matcher.are_related

    def create_dataflows(self, **kwargs) -> List[Dataflow]:
        self.otm = kwargs['otm']
        self.relationships_extractor = kwargs.get('relationships_extractor', None)
        self.are_hierarchically_related = kwargs.get('are_hierarchically_related', None)

        return self.__create_dataflows_by_security_groups()

    def __create_dataflows_by_security_groups(self):
        dataflows = []

        components_in_sgs = self.__match_components_and_sgs()
        if not components_in_sgs:
            return dataflows

        for source_sg, target_sgs in self.__find_sgs_relationships().items():
            if source_sg not in components_in_sgs:
                continue

            for target_sg in target_sgs:
                if target_sg in components_in_sgs:
                    dataflows.extend(
                        self.__create_dataflows_among_components(components_in_sgs[source_sg],
                                                                 components_in_sgs[target_sg]))

        return dataflows

    def __match_components_and_sgs(self) -> Dict[str, List[TFPlanComponent]]:
        components_in_sgs: Dict[str, List[TFPlanComponent]] = {}

        for security_group in self.otm.security_groups:
            components_in_sg = []
            for component in self.otm.components:
                if self.are_component_in_sg(component,
                                            security_group,
                                            relationships_extractor=self.relationships_extractor,
                                            launch_templates=self.otm.launch_templates):
                    components_in_sg.append(component)

            if components_in_sg:
                components_in_sgs[security_group.id] = components_in_sg

        return components_in_sgs

    def __find_sgs_relationships(self) -> Dict[str, List[str]]:
        sgs_relationships: Dict[str, List[str]] = {}

        for source_sg in self.otm.security_groups:
            sg_relationships = []

            for target_sg in self.otm.security_groups:
                if source_sg.id == target_sg.id:
                    continue

                if self.are_sgs_related(source_sg, target_sg, relationships_extractor=self.relationships_extractor):
                    sg_relationships.append(target_sg.id)

            if sg_relationships:
                sgs_relationships[source_sg.id] = list(set(sg_relationships))

        return sgs_relationships

    def __create_dataflows_among_components(self,
                                            source_components: List[TFPlanComponent],
                                            target_components: List[TFPlanComponent]):
        dataflows = []

        for source_component in source_components:
            for target_component in target_components:
                if not self.are_hierarchically_related(source_component, target_component):
                    dataflows.append(create_dataflow(source_component, target_component))

        return dataflows
