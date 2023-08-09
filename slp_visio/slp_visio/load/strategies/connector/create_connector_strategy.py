import abc
from typing import Optional

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector


class CreateConnectorStrategy:
    """
    Formal Interface to create an OTM Dataflow from a vsdx shape
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'create_connector') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def create_connector(self, shape: Shape, components=None) -> Optional[DiagramConnector]:
        """creates the OTM Dataflow from the vsdx shape"""
        raise NotImplementedError


class CreateConnectorStrategyContainer(DeclarativeContainer):
    """
    CreateConnectorStrategy implementations
    """
    visio_strategies = providers.List()
