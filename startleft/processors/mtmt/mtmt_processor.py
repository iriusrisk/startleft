from startleft.processors.base.mapping import MappingLoader, MappingValidator
from startleft.processors.base.otm_processor import OtmProcessor
from startleft.processors.base.provider_loader import ProviderLoader
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.base.provider_validator import ProviderValidator
from startleft.processors.mtmt.mtmt_loader import MtmtLoader
from startleft.processors.mtmt.mtmt_mapping_file_loader import MtmtMappingFileLoader, MtmtMapping
from startleft.processors.mtmt.mtmt_mapping_file_validator import MtmtMappingFileValidator
from startleft.processors.mtmt.mtmt_parser import MtmtParser
from startleft.processors.mtmt.mtmt_validator import MtmtValidator


class MtmtProcessor(OtmProcessor):
    """
    Mtmt implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, source: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return MtmtValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = MtmtLoader(self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return MtmtMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = MtmtMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        mtmt = self.loader.get_mtmt()
        mtmt_mapping = self.mapping_loader.get_mtmt_mapping()
        return MtmtParser(self.project_id, self.project_name, mtmt, mtmt_mapping)
