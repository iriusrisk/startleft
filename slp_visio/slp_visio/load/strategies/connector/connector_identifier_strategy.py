import abc

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from vsdx import Shape


class ConnectorIdentifierStrategy:
    """
    Formal Interface to check if a shape is a connector
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'is_connector') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def is_connector(self, shape: Shape) -> bool:
        """return True if the Shape is a connector"""
        raise NotImplementedError


class ConnectorIdentifierStrategyContainer(DeclarativeContainer):
    """
    ConnectorIdentifierStrategy implementations
    """
    visio_strategies = providers.List()
