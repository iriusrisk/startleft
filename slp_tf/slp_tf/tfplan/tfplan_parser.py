import logging

from networkx import DiGraph

from slp_base import ProviderParser, OTMBuildingError
from slp_tf.slp_tf.tfplan.load.tfplan_launch_templates_loader import TfplanLaunchTemplateLoader
from slp_tf.slp_tf.tfplan.load.tfplan_security_groups_loader import TfplanSecurityGroupsLoader
from slp_tf.slp_tf.tfplan.mapping.tfplan_mapper import TfplanMapper
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanOTM
from slp_tf.slp_tf.tfplan.transformers.tfplan_children_calculator import TfplanChildrenCalculator
from slp_tf.slp_tf.tfplan.transformers.tfplan_dataflow_creator import TfplanDataflowCreator
from slp_tf.slp_tf.tfplan.transformers.tfplan_parent_calculator import TfplanParentCalculator
from slp_tf.slp_tf.tfplan.transformers.tfplan_singleton_transformer import TfplanSingletonTransformer

logger = logging.getLogger(__name__)


class TfplanParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, tfplan: {}, tfgraph: DiGraph, mapping: [{}]):
        self.tfplan = tfplan
        self.tfgraph = tfgraph
        self.mapping = mapping
        self.project_id = project_id
        self.project_name = project_name

        self.otm = TfplanOTM(
            project_id,
            project_name,
            components=[],
            security_groups=[],
            launch_templates=[],
            dataflows=[])

    def build_otm(self):
        try:
            self.__map_tfplan_resources()
            self.__load_auxiliary_resources()

            self.__calculate_parents()
            self.__calculate_children()
            self.__calculate_dataflows()
            self.__calculate_singletons()

        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OTMBuildingError('Error building the threat model with the given files', detail, message)

        return self.otm

    def __map_tfplan_resources(self):
        TfplanMapper(self.otm, self.tfplan, self.mapping).map()

    def __load_auxiliary_resources(self):
        TfplanSecurityGroupsLoader(self.otm, self.tfplan).load()
        TfplanLaunchTemplateLoader(self.otm, self.tfplan).load()

    def __calculate_parents(self):
        TfplanParentCalculator(self.otm, self.tfgraph).transform()

    def __calculate_children(self):
        TfplanChildrenCalculator(self.otm, self.tfgraph).transform()

    def __calculate_dataflows(self):
        TfplanDataflowCreator(self.otm, self.tfgraph).transform()

    def __calculate_singletons(self):
        TfplanSingletonTransformer(self.otm).transform()
