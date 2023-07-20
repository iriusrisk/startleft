import abc

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from vsdx import Shape


class ComponentIdentifierStrategy:
    """
    Formal Interface to check if a shape is a component
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'is_component') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def is_component(self, shape: Shape) -> bool:
        """return True if the Shape is a component"""
        raise NotImplementedError



class ComponentIdentifierStrategyContainer(DeclarativeContainer):
    """
    ComponentIdentifierStrategy implementations is grouped depending on the source tool:
    Lucid or Visio
    """
    visio_strategies = providers.List()