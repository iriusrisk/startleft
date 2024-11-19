from networkx import DiGraph

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM
from slp_tfplan.slp_tfplan.transformers.hierarchy_calculator import HierarchyCalculator

PARENT_TYPES = {
   'subnets': ['aws_subnet', 'azurerm_subnet'],
   'vpcs': ['aws_vpc', 'azurerm_virtual_network']
}

class ParentCalculator(HierarchyCalculator):

    def __init__(self, otm: TFPlanOTM, graph: DiGraph):
        super().__init__(otm, graph)
        self.subnet_candidates = self._find_components_by_type(PARENT_TYPES['subnets'])
        self.vpc_candidates = self._find_components_by_type(PARENT_TYPES['vpcs'])

    def _calculate_component_parents(self, component: TFPlanComponent) -> [str]:
       return self._find_parent_by_closest_relationship(component, self.subnet_candidates) or \
                self._find_parent_by_closest_relationship(component, self.vpc_candidates)
