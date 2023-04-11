import abc

from vsdx import Shape

from otm.otm.entity.dataflow import Dataflow
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
    def create_connector(self, shape: Shape) -> Dataflow:
        """creates the OTM Dataflow from the vsdx shape"""
        raise NotImplementedError
