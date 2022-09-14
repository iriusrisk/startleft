from slp_base import MappingLoader, MappingValidator
from slp_base import OtmProcessor
from slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_validator import MTMTMappingFileValidator
from slp_mtmt.slp_mtmt.mtmt_parser import MTMTParser
from slp_mtmt.slp_mtmt.mtmt_validator import MTMTValidator


class MTMTProcessor(OtmProcessor):
    """
    MTMT implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, source: [bytes], mappings: [bytes]):
        self.mtmt = None
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings

    def get_provider_validator(self) -> ProviderValidator:
        return MTMTValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        loader = MTMTLoader(self.source)
        self.mtmt = loader.get_mtmt()
        return loader

    def get_mapping_validator(self) -> MappingValidator:
        return MTMTMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        return MTMTMappingFileLoader(self.mappings)

    def get_provider_parser(self) -> ProviderParser:
        return MTMTParser(self.project_id, self.project_name, self.mtmt, self.mappings)
