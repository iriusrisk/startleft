import abc

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import List


class MatchStrategy:
    """
    Interface which defines different strategies to identify if two resources are related between them.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'are_related') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def are_related(self, resource_1, resource_2, **kwargs) -> bool:
        """
        Common method to identify if two resources are related.
        Two resources may be related in different ways (by the tfgraph, by configuration, by intermediate resources, etc.).
        Each implementation of the `MatchStrategy` class defines the logic to identify the potential relationship.
        :param resource_1: The first resource to relate.
        :param resource_2: The second resource to relate.
        :param kwargs: An unbounded list of parameters potentially required by the strategies to find the relationship.
        :return: True if there is a relationships, not otherwise.
        """
        raise NotImplementedError


class MatchStrategyContainer(DeclarativeContainer):
    """
    `MatchStrategy` implementations tend to be grouped depending on the type of resources they relate.
    For example, there are a group of implementations to identify relationships between Security Groups and Components
    and another group to find relationships between one Security Group and another.
    Here are defined a list of instances for each of these groups.
    """

    sg_sg_match_strategies = List()
    sg_sg_rule_match_strategies = List()
    component_sg_match_strategies = List()
