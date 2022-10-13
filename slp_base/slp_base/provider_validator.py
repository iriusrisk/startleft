import abc


class ProviderValidator(metaclass=abc.ABCMeta):
    """
    Formal Interface to validate the provider source data
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'validate') and callable(subclass.validate)
                or NotImplemented)

    @abc.abstractmethod
    def validate(self):
        """Validate source provider data"""
        raise NotImplementedError
