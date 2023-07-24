import abc

from vsdx import Shape

from slp_visio.slp_visio.load.strategies.strategy import Strategy


class BoundaryIdentifierStrategy(Strategy):
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
