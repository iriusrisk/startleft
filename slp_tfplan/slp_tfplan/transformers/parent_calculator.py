from networkx import DiGraph

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TfplanOTM
from slp_tfplan.slp_tfplan.transformers.hierarchy_calculator import HierarchyCalculator

PARENT_TYPES = ['aws_subnet', 'aws_vpc', 'azurerm_subnet', 'azurerm_virtual_network']


class ParentCalculator(HierarchyCalculator):

    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)
        self.parent_candidates = self._get_parent_candidates(PARENT_TYPES)

    def _calculate_component_parents(self, component: TFPlanComponent) -> [str]:
        return self._find_parent_by_closest_relationship(component, self.parent_candidates)


