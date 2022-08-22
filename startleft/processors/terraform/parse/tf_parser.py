from startleft.iac.iac_type import IacType

from startleft.otm.otm import OTM
from startleft.otm.otm_builder import OtmBuilder
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.terraform.parse.mapping.tf_sourcemodel import TerraformSourceModel
from startleft.processors.terraform.parse.mapping.tf_transformer import TerraformTransformer


class TerraformParser(ProviderParser):
    """
    Parser to build an OTM from Terraform
    """

    def __init__(self, project_id: str, project_name: str, source, mapping: [str]):
        self.source = source
        self.mapping = mapping
        self.project_id = project_id
        self.project_name = project_name

        self.otm = self.__initialize_otm()
        self.source_model = TerraformSourceModel()
        self.source_model.data = self.source
        self.source_model.otm = self.otm
        self.transformer = TerraformTransformer(source_model=self.source_model, threat_model=self.otm)

    def build_otm(self) -> OTM:
        self.transformer.run(self.mapping)
        return self.otm

    def __initialize_otm(self):
        return OtmBuilder(self.project_id, self.project_name, IacType.TERRAFORM).build()
