import abc


class MappingLoader(metaclass=abc.ABCMeta):
    """
    Formal Interface to load the mapping data
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'load') and callable(subclass.load)
                or NotImplemented)

    @abc.abstractmethod
    def load(self):
        """Load mapping data"""
        raise NotImplementedError
