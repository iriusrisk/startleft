import abc

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from vsdx import Shape



class BoundaryIdentifierStrategy:
    """
    Formal Interface to check if a shape is a boundary
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'is_boundary') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def is_boundary(self, shape: Shape) -> bool:
        """return True if the Shape is a boundary"""
        raise NotImplementedError

class BoundaryIdentifierStrategyContainer(DeclarativeContainer):
    """
    ComponentIdentifierStrategy implementations
    """
    visio_strategies = providers.List()