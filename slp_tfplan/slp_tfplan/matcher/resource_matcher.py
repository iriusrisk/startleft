from typing import List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer


class ResourceMatcher:
    """
    Class which defines a method to find if two resources are related.
    """

    def __init__(self, strategies: List[MatchStrategy]):
        self.strategies = strategies

    def are_related(self, resource_1, resource_2, **kwargs) -> bool:
        """
        Method to identify if two resources are related based on any kind of logic. It relies on a set of strategies
        to check if the relationship exists. If any of them identify a relationships, the method returns True, otherwise
        it returns False.
        :param resource_1: The first resource to relate.
        :param resource_2: The second resource to relate.
        :param kwargs: An unbounded list of parameters potentially required by the strategies to find the relationship.
        :return: True if there is a relationships, not otherwise.
        """
        for strategy in self.strategies:
            if strategy.are_related(resource_1, resource_2, **kwargs):
                return True

        return False


class ResourcesMatcherContainer(DeclarativeContainer):
    """
    `ResourcesMatcher` is a generic class to find relationships between any kind of resources. Depending on the
    strategies we pass as parameters to the class, it will find relationships between different types of resources.
    For each of these types of relationship, here is defined an instance to be injected using dependency-injector
    (see https://python-dependency-injector.ets-labs.org/)
    """

    sgs_resources_matcher = providers.Singleton(
        ResourceMatcher,
        strategies=MatchStrategyContainer.sg_match_strategies
    )

    component_sg_matcher = providers.Singleton(
        ResourceMatcher,
        strategies=MatchStrategyContainer.component_sg_match_strategies
    )
