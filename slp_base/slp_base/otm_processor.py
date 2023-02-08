import abc

from otm.otm.entity.otm import Otm
from slp_base.slp_base.mapping import MappingLoader, MappingValidator
from slp_base.slp_base.otm_representations_pruner import OtmRepresentationsPruner
from slp_base.slp_base.otm_trustzone_unifier import OtmTrustZoneUnifier
from slp_base.slp_base.otm_validator import OtmValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_validator import ProviderValidator


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
    def process(self) -> Otm:
        """Process all the flow from the input data to the OTM output"""
        self.get_provider_validator().validate()
        self.get_provider_loader().load()

        self.get_mapping_validator().validate()
        self.get_mapping_loader().load()

        otm = self.get_provider_parser().build_otm()

        OtmRepresentationsPruner(otm).prune()
        OtmTrustZoneUnifier(otm).unify()
        OtmValidator().validate(otm.json())

        return otm

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
