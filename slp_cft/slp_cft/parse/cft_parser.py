import logging

from otm.otm.otm import OTM
from otm.otm.otm_builder import OtmBuilder
from slp_base.slp_base.errors import OtmBuildingError
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import IacType
from slp_cft.slp_cft.parse.mapping.cft_path_ids_calculator import CloudformationPathIdsCalculator
from slp_cft.slp_cft.parse.mapping.cft_sourcemodel import CloudformationSourceModel
from slp_cft.slp_cft.parse.mapping.cft_transformer import CloudformationTransformer

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
        self.source_model = CloudformationSourceModel(self.source, self.otm)
        self.transformer = CloudformationTransformer(source_model=self.source_model, threat_model=self.otm)

    def build_otm(self) -> OTM:
        try:
            self.transformer.run(self.mapping)
            self.__set_full_path_in_ids()
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OtmBuildingError('Error building the threat model with the given files', detail, message)

        return self.otm

    def __initialize_otm(self):
        return OtmBuilder(self.project_id, self.project_name, IacType.CLOUDFORMATION).build()

    def __set_full_path_in_ids(self):
        path_ids = CloudformationPathIdsCalculator(self.otm.components).calculate_path_ids()

        self.__update_component_ids(path_ids)
        self.__update_dataflow_ids(path_ids)

    def __update_component_ids(self, path_ids: {}):
        for component in self.otm.components:
            if component.id in path_ids:
                component.id = path_ids[component.id]
            if component.parent in path_ids:
                component.parent = path_ids[component.parent]

    def __update_dataflow_ids(self, path_ids: {}):
        for dataflow in self.otm.dataflows:
            if dataflow.source_node in path_ids:
                dataflow.source_node = path_ids[dataflow.source_node]
            if dataflow.destination_node in path_ids:
                dataflow.destination_node = path_ids[dataflow.destination_node]
