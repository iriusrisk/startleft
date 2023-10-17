import abc

from otm.otm.entity.otm import OTM
from otm.otm.otm_pruner import OTMPruner
from slp_base.slp_base.mapping import MappingLoader, MappingValidator
from slp_base.slp_base.otm_representations_pruner import OTMRepresentationsPruner
from slp_base.slp_base.otm_validator import OTMValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_validator import ProviderValidator


class OTMProcessor(metaclass=abc.ABCMeta):
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
    def process(self) -> OTM:
        """Process all the flow from the input data to the OTM output"""
        try:
            self.get_provider_validator().validate()
            self.get_provider_loader().load()

            self.get_mapping_validator().validate()
            self.get_mapping_loader().load()

            otm = self.get_provider_parser().build_otm()
            OTMPruner(otm).prune_orphan_dataflows()
            OTMPruner(otm).prune_self_reference_dataflows()
        finally:
            self._clean_resources()

        OTMRepresentationsPruner(otm).prune()
        OTMValidator().validate(otm.json())

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

    def _clean_resources(self):
        """hook method to let the subclasses clean up its resources if necessary"""
        pass
