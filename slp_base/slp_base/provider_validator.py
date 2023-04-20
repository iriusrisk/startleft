import abc

from otm.otm.provider import Provider
from slp_base.slp_base.errors import SourceFileNotValidError


def generate_content_type_error(provider: Provider, source_file_name: str, exception=SourceFileNotValidError):
    title = f'{provider.provider_name} file is not valid'
    details = f'Invalid content type for {source_file_name}'
    msg = details
    return exception(title, msg, msg)


def generate_size_error(provider: Provider, source_file_name: str, exception=SourceFileNotValidError):
    title = f'{provider.provider_name} file is not valid'
    details = f'Provided {source_file_name} is not valid. Invalid size'
    msg = details
    return exception(title, msg, msg)


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
