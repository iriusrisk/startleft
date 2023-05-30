import abc

from vsdx import Shape

from slp_visio.slp_visio.load.strategies.strategy import Strategy


class ComponentIdentifierStrategy(Strategy):
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
