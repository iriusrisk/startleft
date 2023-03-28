from starlette.datastructures import UploadFile

from sl_util.sl_util.file_utils import copy_to_disk, delete
from slp_base import OTMProcessor, ProviderValidator, ProviderLoader, MappingValidator, MappingLoader, ProviderParser, \
    DiagramType
from slp_visio.slp_visio.load.visio_loader import VisioLoader
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.lucid.load.lucid_loader import LucidLoader
from slp_visio.slp_visio.lucid.parse.lucid_parser import LucidParser
from slp_visio.slp_visio.lucid.validate.lucid_validator import LucidValidator
from slp_visio.slp_visio.parse.visio_parser import VisioParser
from slp_visio.slp_visio.validate.visio_mapping_file_validator import VisioMappingFileValidator
from slp_visio.slp_visio.validate.visio_validator import VisioValidator


class VisioProcessor(OTMProcessor):
    """
    Visio implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, source, mappings: [bytes], diag_type=None):
        self.diag_type = diag_type if diag_type else DiagramType.VISIO
        self.project_id = project_id
        self.project_name = project_name
        self.mappings = mappings
        self.is_temporary_source = type(source) is UploadFile
        self.source = copy_to_disk(source.file, '.vsdx') if self.is_temporary_source else source
        self.loader = None
        self.mapping_loader = None

    def __del__(self):
        if self.is_temporary_source:
            delete(self.source.name)

    def get_provider_validator(self) -> ProviderValidator:
        if self.diag_type == DiagramType.LUCID:
            return LucidValidator(self.source)
        else:
            return VisioValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        if self.diag_type == DiagramType.LUCID:
            self.loader = LucidLoader(self.source)
        else:
            self.loader = VisioLoader(self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return VisioMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = VisioMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        visio = self.loader.get_visio()
        if self.diag_type == DiagramType.LUCID:
            return LucidParser(self.project_id, self.project_name, visio, self.mapping_loader)
        else:
            return VisioParser(self.project_id, self.project_name, visio, self.mapping_loader)
