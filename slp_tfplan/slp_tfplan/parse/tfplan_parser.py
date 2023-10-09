import logging

from networkx import DiGraph

from slp_base import ProviderParser, OTMBuildingError
from slp_tfplan.slp_tfplan.load.launch_templates_loader import LaunchTemplatesLoader
from slp_tfplan.slp_tfplan.load.security_groups_loader import SecurityGroupsLoader
from slp_tfplan.slp_tfplan.load.variables_loader import VariablesLoader
from slp_tfplan.slp_tfplan.map.mapping import Mapping
from slp_tfplan.slp_tfplan.map.tfplan_mapper import TFPlanMapper
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM
from slp_tfplan.slp_tfplan.transformers.attack_surface_calculator import AttackSurfaceCalculator
from slp_tfplan.slp_tfplan.transformers.children_calculator import ChildrenCalculator
from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator import DataflowCreator
from slp_tfplan.slp_tfplan.transformers.parent_calculator import ParentCalculator
from slp_tfplan.slp_tfplan.transformers.singleton_transformer import SingletonTransformer

logger = logging.getLogger(__name__)


class TFPlanParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, tfplan: {}, tfgraph: DiGraph, mapping: Mapping):
        self.tfplan = tfplan
        self.tfgraph = tfgraph
        self.mapping = mapping
        self.project_id = project_id
        self.project_name = project_name

        self.otm = TFPlanOTM(
            project_id,
            project_name,
            components=[],
            security_groups=[],
            launch_templates=[],
            variables={},
            dataflows=[])

    def build_otm(self):
        try:
            self.__map_tfplan_resources()
            self.__load_auxiliary_resources()

            self.__calculate_parents()
            self.__calculate_children()
            self.__calculate_dataflows()
            self.__calculate_attack_surface()
            self.__calculate_singletons()

        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise OTMBuildingError('Error building the threat model with the given files', detail, message)

        return self.otm

    def __map_tfplan_resources(self):
        TFPlanMapper(self.otm, self.tfplan, self.mapping).map()

    def __load_auxiliary_resources(self):
        SecurityGroupsLoader(self.otm, self.tfplan, self.tfgraph).load()
        LaunchTemplatesLoader(self.otm, self.tfplan).load()
        VariablesLoader(self.otm, self.tfplan).load()

    def __calculate_parents(self):
        ParentCalculator(self.otm, self.tfgraph).transform()

    def __calculate_children(self):
        ChildrenCalculator(self.otm, self.tfgraph).transform()

    def __calculate_dataflows(self):
        DataflowCreator(self.otm, self.tfgraph).transform()

    def __calculate_attack_surface(self):
        AttackSurfaceCalculator(self.otm, self.tfgraph, self.mapping.attack_surface) .transform()

    def __calculate_singletons(self):
        SingletonTransformer(self.otm).transform()
