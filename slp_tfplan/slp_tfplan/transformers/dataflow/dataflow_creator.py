import uuid
from typing import List

from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.component_security_group_match_strategies import \
    ComponentSecurityGroupMatchStrategy
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourcesMatcher
from slp_tfplan.slp_tfplan.matcher.security_group_match_strategies import SecurityGroupMatchStrategy
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent
from slp_tfplan.slp_tfplan.strategy.strategy import get_strategies
from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_strategies import DataflowCreationStrategy
from slp_tfplan.slp_tfplan.transformers.transformer import Transformer


def create_dataflow(source_component: TFPlanComponent, target_component: TFPlanComponent, bidirectional: bool = False):
    return Dataflow(
        # TODO Generate deterministic ID
        dataflow_id=str(uuid.uuid4()),
        name=f'{source_component.name} to {target_component.name}',
        source_node=source_component.id,
        destination_node=target_component.id,
        bidirectional=bidirectional
    )


def find_component_by_id(component_id: str, components: List[TFPlanComponent]):
    return next(filter(lambda c: c.id == component_id, components))


class DataflowCreator(Transformer):

    def __init__(self, otm: TFPlanOTM, graph: DiGraph):
        super().__init__(otm, graph)

        self.components: [TFPlanComponent] = otm.components
        self.dataflows: [Dataflow] = otm.dataflows

        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=graph)

        self.strategies = get_strategies(DataflowCreationStrategy)

    def transform(self):
        for strategy in self.strategies:
            self.dataflows.extend(strategy.create_dataflows(
                otm=self.otm,
                relationships_extractor=self.relationships_extractor,

                are_hierarchically_related=self._are_hierarchically_related,
                are_component_in_sg=ResourcesMatcher(ComponentSecurityGroupMatchStrategy).are_related,
                are_sgs_related=ResourcesMatcher(SecurityGroupMatchStrategy).are_related))

    # TODO Refactor to an specific class
    def _are_hierarchically_related(self, first: TFPlanComponent, second: TFPlanComponent) -> bool:
        return first.id == second.id or \
            self.__is_ancestor(first, second) or self.__is_ancestor_of_any_clone(first, second) \
            or self.__is_ancestor(second, first) or self.__is_ancestor_of_any_clone(second, first)

    def __is_ancestor(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        return component.parent_type == ParentType.COMPONENT and \
            (component.parent == ancestor.id
             or self.__is_ancestor(find_component_by_id(component.parent, self.components), ancestor))

    def __is_ancestor_of_any_clone(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        if not component.clones_ids:
            return False

        for clone_id in component.clones_ids:
            if self.__is_ancestor(find_component_by_id(clone_id, self.components), ancestor):
                return True

        return False
