from slp_base import MappingLoader, MappingValidator
from slp_base import OTMProcessor
from slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_validator import MTMTMappingFileValidator
from slp_mtmt.slp_mtmt.mtmt_parser import MTMTParser
from slp_mtmt.slp_mtmt.mtmt_validator import MTMTValidator


class MTMTProcessor(OTMProcessor):
    """
    Mtmt implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, source: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return MTMTValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = MTMTLoader(self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return MTMTMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = MTMTMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        mtmt = self.loader.get_mtmt()
        mtmt_mapping = self.mapping_loader.get_mtmt_mapping()
        return MTMTParser(self.project_id, self.project_name, mtmt, mtmt_mapping)
