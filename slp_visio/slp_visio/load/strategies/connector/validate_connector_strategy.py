import abc

from vsdx import Shape

from slp_visio.slp_visio.load.strategies.strategy import Strategy


class ValidateConnectorStrategy(Strategy):
    """
    Formal Interface to validate if a shape is a connector
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
