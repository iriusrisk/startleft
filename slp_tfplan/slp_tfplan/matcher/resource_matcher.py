from typing import List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer


class ResourcesMatcher:

    def __init__(self, strategies: List[MatchStrategy]):
        self.strategies = strategies

    def are_related(self, object_1, object_2, **kwargs) -> bool:
        for strategy in self.strategies:
            if strategy.are_related(object_1, object_2, **kwargs):
                return True

        return False


class ResourcesMatcherContainer(DeclarativeContainer):
    sgs_resources_matcher = providers.Singleton(
        ResourcesMatcher,
        strategies=MatchStrategyContainer.sg_match_strategies
    )

    component_sg_matcher = providers.Singleton(
        ResourcesMatcher,
        strategies=MatchStrategyContainer.component_sg_match_strategies
    )
