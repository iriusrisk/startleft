import abc


class ProviderLoader(metaclass=abc.ABCMeta):
    """
    Formal Interface to load the provider source data
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'load') and callable(subclass.load)
                or NotImplemented)

    @abc.abstractmethod
    def load(self):
        """Load source provider data"""
        raise NotImplementedError
