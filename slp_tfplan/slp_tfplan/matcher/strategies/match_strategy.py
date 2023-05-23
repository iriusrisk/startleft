import abc

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import List


class MatchStrategy:
    # TODO Create documentation per strategy group

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'are_related') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def are_related(self, object_1, object_2, **kwargs):
        raise NotImplementedError


class MatchStrategyContainer(DeclarativeContainer):
    sg_match_strategies = List()
    component_sg_match_strategies = List()
