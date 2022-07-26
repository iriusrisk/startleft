import abc


class MappingValidator(metaclass=abc.ABCMeta):
    """
    Formal Interface to validate a mapping file
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'validate') and callable(subclass.validate)
                or NotImplemented)

    @abc.abstractmethod
    def validate(self):
        """Validate mapping file"""
        raise NotImplementedError
