from slp_base.slp_base import MappingLoader, MappingValidator
from slp_base.slp_base import OtmProcessor
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_tf.slp_tf.load.tf_loader import TerraformLoader
from slp_tf.slp_tf.load.tfplan_loader import TfplanLoader, is_tfplan
from slp_tf.slp_tf.load.tf_mapping_file_loader import TerraformMappingFileLoader
from slp_tf.slp_tf.parse.tf_parser import TerraformParser
from slp_tf.slp_tf.validate.tf_mapping_file_validator import TerraformMappingFileValidator
from slp_tf.slp_tf.validate.tf_validator import TerraformValidator


class TerraformProcessor(OtmProcessor):
    """
    Terraform implementation of OtmProcessor
    """

    def __init__(self, project_id: str, project_name: str, sources: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.sources = sources
        self.mappings = mappings

        self.terraform_loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return TerraformValidator(self.sources)

    def get_provider_loader(self) -> ProviderLoader:
        self.terraform_loader = \
            TfplanLoader(self.sources[0]) if is_tfplan(self.sources) else TerraformLoader(self.sources)
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
