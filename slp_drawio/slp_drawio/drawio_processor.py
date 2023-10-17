from slp_base import OTMProcessor, ProviderValidator, ProviderLoader, MappingValidator, MappingLoader, ProviderParser, \
    DiagramType
from slp_drawio.slp_drawio.load.drawio_loader import DrawioLoader
from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMappingFileLoader
from slp_drawio.slp_drawio.parse.drawio_parser import DrawioParser
from slp_drawio.slp_drawio.validate.drawio_mapping_file_validator import DrawioMappingFileValidator
from slp_drawio.slp_drawio.validate.drawio_validator import DrawioValidator


class DrawioProcessor(OTMProcessor):
    """
    Drawio implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, source, mappings: [bytes],  diag_type=None):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return DrawioValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = DrawioLoader(self.project_id, self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return DrawioMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = DrawioMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        drawio = self.loader.get_diagram()
        drawio_mapping = self.mapping_loader.get_mappings()
        return DrawioParser(self.project_id, self.project_name, drawio, drawio_mapping)
