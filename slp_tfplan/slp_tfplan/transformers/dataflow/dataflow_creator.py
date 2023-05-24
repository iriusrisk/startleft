from typing import List

from dependency_injector.wiring import Provide, inject
from networkx import DiGraph

from otm.otm.entity.parent_type import ParentType
from sl_util.sl_util.iterations_utils import remove_duplicates
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    DataflowCreationStrategyContainer
from slp_tfplan.slp_tfplan.transformers.transformer import Transformer


def find_component_by_id(component_id: str, components: List[TFPlanComponent]):
    return next(filter(lambda c: c.id == component_id, components))


class DataflowCreator(Transformer):

    @inject
    def __init__(self,
                 otm: TFPlanOTM,
                 graph: DiGraph,
                 strategies: List[DataflowCreationStrategy] = Provide[
                     DataflowCreationStrategyContainer.strategies]):
        super().__init__(otm, graph)

        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=graph)

        self.strategies = strategies

    def transform(self):
        for strategy in self.strategies:
            self.otm.dataflows.extend(strategy.create_dataflows(
                otm=self.otm,
                relationships_extractor=self.relationships_extractor,
                are_hierarchically_related=self._are_hierarchically_related))

        self.otm.dataflows = remove_duplicates(self.otm.dataflows)

    def _are_hierarchically_related(self, first: TFPlanComponent, second: TFPlanComponent) -> bool:
        return first.id == second.id or \
            self.__is_ancestor(first, second) or self.__is_ancestor_of_any_clone(first, second) \
            or self.__is_ancestor(second, first) or self.__is_ancestor_of_any_clone(second, first)

    def __is_ancestor(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        return component.parent_type == ParentType.COMPONENT and \
            (component.parent == ancestor.id
             or self.__is_ancestor(find_component_by_id(component.parent, self.otm.components), ancestor))

    def __is_ancestor_of_any_clone(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        if not component.clones_ids:
            return False

        for clone_id in component.clones_ids:
            if self.__is_ancestor(find_component_by_id(clone_id, self.otm.components), ancestor):
                return True

        return False
