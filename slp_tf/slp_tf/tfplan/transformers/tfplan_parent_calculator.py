from networkx import DiGraph

from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanComponent, TfplanOTM
from slp_tf.slp_tf.tfplan.transformers.hierarchy_calculator import HierarchyCalculator

PARENT_TYPES = ['aws_subnet', 'aws_vpc']


class TfplanParentCalculator(HierarchyCalculator):

    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)
        self.parent_candidates = self._get_parent_candidates(PARENT_TYPES)

    def _calculate_component_parents(self, component: TfplanComponent) -> [str]:
        return self._find_parent_by_closest_relationship(component, self.parent_candidates)


