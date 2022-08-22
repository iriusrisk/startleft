from startleft.processors.base.mapping import MappingLoader, MappingValidator
from startleft.processors.base.otm_processor import OtmProcessor
from startleft.processors.base.provider_loader import ProviderLoader
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.base.provider_validator import ProviderValidator
from startleft.processors.terraform.load.tf_loader import TerraformLoader
from startleft.processors.terraform.load.tf_mapping_file_loader import TerraformMappingFileLoader
from startleft.processors.terraform.parse.tf_parser import TerraformParser
from startleft.processors.terraform.validate.tf_mapping_file_validator import TerraformMappingFileValidator
from startleft.processors.terraform.validate.tf_validator import TerraformValidator


class TerraformProcessor(OtmProcessor):
    """
    Terraform implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, source: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mappings = mappings

        self.terraform_loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return TerraformValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.terraform_loader = TerraformLoader(self.source)
        return self.terraform_loader

    def get_mapping_validator(self) -> MappingValidator:
        return TerraformMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = TerraformMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        return TerraformParser(
            self.project_id,
            self.project_name,
            self.terraform_loader.get_terraform(),
            self.mapping_loader.get_mappings())
