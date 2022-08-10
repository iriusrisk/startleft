import abc

from startleft.otm.otm import OTM
from startleft.processors.base.mapping import MappingLoader, MappingValidator
from startleft.processors.base.provider_loader import ProviderLoader
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.base.provider_validator import ProviderValidator


class OtmProcessor(metaclass=abc.ABCMeta):
    """
    Formal Interface to manage all the flow from the input data to the OTM output
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'process') and callable(subclass.process)
                and hasattr(subclass, 'get_provider_validator') and callable(subclass.get_provider_validator)
                and hasattr(subclass, 'get_provider_loader') and callable(subclass.get_provider_loader)
                and hasattr(subclass, 'get_mapping_validator') and callable(subclass.get_mapping_validator)
                and hasattr(subclass, 'get_mapping_loader') and callable(subclass.get_mapping_loader)
                and hasattr(subclass, 'get_provider_parser') and callable(subclass.get_provider_parser)
                or NotImplemented)

    # Do not override this method.
    def process(self, project_id: str, project_name: str) -> OTM:
        """Process all the flow from the input data to the OTM output"""
        self.get_provider_validator().validate()
        self.get_provider_loader().load()
        self.get_mapping_validator().validate()
        #self.get_mapping_loader().load()
        return self.get_provider_parser().build_otm(project_id, project_name)

    @abc.abstractmethod
    def get_provider_validator(self) -> ProviderValidator:
        """get the provider validator implementation"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_provider_loader(self) -> ProviderLoader:
        """get the provider loader implementation"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_mapping_validator(self) -> MappingValidator:
        """get the mapping validator implementation"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_mapping_loader(self) -> MappingLoader:
        """get the mapping loader implementation"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_provider_parser(self) -> ProviderParser:
        """get the provider parser implementation to build the otm"""
        raise NotImplementedError
