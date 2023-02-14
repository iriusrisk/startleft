from slp_base.slp_base import MappingLoader, MappingValidator
from slp_base.slp_base import OTMProcessor
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_cft.slp_cft.load.cft_loader import CloudformationLoader
from slp_cft.slp_cft.load.cft_mapping_file_loader import CloudformationMappingFileLoader
from slp_cft.slp_cft.parse.cft_parser import CloudformationParser
from slp_cft.slp_cft.validate.cft_mapping_file_validator import \
    CloudformationMappingFileValidator
from slp_cft.slp_cft.validate.cft_validator import CloudformationValidator


class CloudformationProcessor(OTMProcessor):
    """
    Cloudformation implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, sources: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.sources = sources
        self.mappings = mappings

        self.cloudformation_loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return CloudformationValidator(self.sources)

    def get_provider_loader(self) -> ProviderLoader:
        self.cloudformation_loader = CloudformationLoader(self.sources)
        return self.cloudformation_loader

    def get_mapping_validator(self) -> MappingValidator:
        return CloudformationMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = CloudformationMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        return CloudformationParser(
            self.project_id,
            self.project_name,
            self.cloudformation_loader.get_cloudformation(),
            self.mapping_loader.get_mappings())
