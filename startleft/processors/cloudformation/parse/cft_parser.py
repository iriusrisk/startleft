import logging

from startleft.api.errors import OtmBuildingError
from startleft.iac.iac_type import IacType
from startleft.otm.otm import OTM
from startleft.otm.otm_builder import OtmBuilder
from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.cloudformation.parse.mapping.cft_sourcemodel import CloudformationSourceModel
from startleft.processors.cloudformation.parse.mapping.cft_transformer import CloudformationTransformer

logger = logging.getLogger(__name__)


class CloudformationParser(ProviderParser):
    """
    Parser to build an OTM from CloudFormation
    """

    def __init__(self, project_id: str, project_name: str, source, mapping: [str]):
        self.source = source
        self.mapping = mapping
        self.project_id = project_id
        self.project_name = project_name

        self.otm = self.__initialize_otm()
        self.source_model = CloudformationSourceModel()
        self.source_model.data = self.source
        self.source_model.otm = self.otm
        self.transformer = CloudformationTransformer(source_model=self.source_model, threat_model=self.otm)

    def build_otm(self) -> OTM:
        try:
            self.transformer.run(self.mapping)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OtmBuildingError('Error building the threat model with the given files', detail, message)

        return self.otm

    def __initialize_otm(self):
        return OtmBuilder(self.project_id, self.project_name, IacType.CLOUDFORMATION).build()
