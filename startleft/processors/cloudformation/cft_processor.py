from startleft.processors.base.mapping import MappingLoader, MappingValidator
from startleft.processors.base.otm_processor import OtmProcessor
from startleft.processors.base.provider_loader import ProviderLoader
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.base.provider_validator import ProviderValidator
from startleft.processors.cloudformation.load.cft_loader import CloudformationLoader
from startleft.processors.cloudformation.load.cft_mapping_file_loader import CloudformationMappingFileLoader
from startleft.processors.cloudformation.parse.cft_parser import CloudformationParser
from startleft.processors.cloudformation.validate.cft_mapping_file_validator import CloudformationMappingFileValidator
from startleft.processors.cloudformation.validate.cft_validator import CloudformationValidator


class CloudformationProcessor(OtmProcessor):
    """
    Cloudformation implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, source: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings

        self.cloudformation_loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return CloudformationValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.cloudformation_loader = CloudformationLoader(self.source)
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
