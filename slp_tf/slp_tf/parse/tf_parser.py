import logging

from otm.otm.otm import OTM
from otm.otm.otm_builder import OtmBuilder
from slp_base import OtmBuildingError
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import IacType
from slp_tf.slp_tf.parse.mapping.tf_component_id_generator import TerraformComponentIdGenerator
from slp_tf.slp_tf.parse.mapping.tf_path_ids_calculator import TerraformPathIdsCalculator
from slp_tf.slp_tf.parse.mapping.tf_sourcemodel import TerraformSourceModel
from slp_tf.slp_tf.parse.mapping.tf_transformer import TerraformTransformer

logger = logging.getLogger(__name__)


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
        try:
            self.transformer.run(self.mapping)

            self.__set_path_ids()
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OtmBuildingError('Error building the threat model with the given files', detail, message)

        return self.otm

    def __initialize_otm(self):
        return OtmBuilder(self.project_id, self.project_name, IacType.TERRAFORM).build()

    def __set_path_ids(self):
        path_ids = TerraformPathIdsCalculator(self.otm.components, TerraformComponentIdGenerator).calculate_path_ids()

        self.__replace_component_ids(path_ids)
        self.__replace_dataflow_ids(path_ids)

    def __replace_component_ids(self, path_ids: {}):
        for component in self.otm.components:
            if component.id in path_ids:
                component.id = path_ids[component.id]
            if component.parent in path_ids:
                component.parent = path_ids[component.parent]

    def __replace_dataflow_ids(self, path_ids: {}):
        for dataflow in self.otm.dataflows:
            if dataflow.source_node in path_ids:
                dataflow.source_node = path_ids[dataflow.source_node]
            if dataflow.destination_node in path_ids:
                dataflow.destination_node = path_ids[dataflow.destination_node]
