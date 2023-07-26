import logging
from typing import List

from dependency_injector.wiring import Provide, inject
from networkx import DiGraph

from sl_util.sl_util.iterations_utils import remove_duplicates
from sl_util.sl_util.lang_utils import get_class_name
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    DataflowCreationStrategyContainer
from slp_tfplan.slp_tfplan.transformers.transformer import Transformer

logger = logging.getLogger(__name__)


def _log_applied_strategy(number_of_dataflows: int, strategy_applied: str):
    logger.debug(f'Found {number_of_dataflows} dataflows using {strategy_applied}')


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
            strategy_dataflows = strategy.create_dataflows(
                otm=self.otm, relationships_extractor=self.relationships_extractor)

            if strategy_dataflows:
                _log_applied_strategy(len(strategy_dataflows), get_class_name(strategy))
                self.otm.dataflows.extend(strategy_dataflows)

        self.otm.dataflows = remove_duplicates(self.otm.dataflows)
