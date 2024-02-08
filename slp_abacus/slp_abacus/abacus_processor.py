from starlette.datastructures import UploadFile

from sl_util.sl_util.file_utils import get_byte_data, get_byte_data_from_upload_file
from slp_abacus.slp_abacus.load.abacus_loader import AbacusLoader
from slp_abacus.slp_abacus.load.abacus_mapping_file_loader import AbacusMappingFileLoader
from slp_abacus.slp_abacus.parse.abacus_parser import AbacusParser
from slp_abacus.slp_abacus.validate.abacus_mapping_file_validator import AbacusMappingFileValidator
from slp_abacus.slp_abacus.validate.abacus_validator import AbacusValidator
from slp_base import OTMProcessor, ProviderValidator, ProviderLoader, MappingValidator, MappingLoader, ProviderParser


class AbacusProcessor(OTMProcessor):
    """
    Abacus implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, source, mappings: [bytes], diag_type=None):
        self.project_id = project_id
        self.project_name = project_name
        self.source: bytes = \
            get_byte_data_from_upload_file(source) if isinstance(source, UploadFile) else get_byte_data(source.name)
        self.mappings = mappings
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return AbacusValidator()

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = AbacusLoader(self.project_id, self.source, self.mappings)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return AbacusMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = AbacusMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        abacus = self.loader.get_diagram()
        abacus_mapping = self.mapping_loader.get_mappings()
        return AbacusParser(self.project_id, self.project_name, abacus, abacus_mapping)
