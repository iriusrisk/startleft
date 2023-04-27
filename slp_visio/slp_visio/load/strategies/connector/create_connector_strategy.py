import abc
from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.strategies.strategy import Strategy


class CreateConnectorStrategy(Strategy):
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
