import abc
from copy import deepcopy

from networkx import DiGraph

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TfplanOTM
from slp_tfplan.slp_tfplan.transformers.transformer import Transformer


def clone_component_by_parents(component: TFPlanComponent, parent_ids: [str]) -> [{}]:
    clones = []

    for index, parent_id in enumerate(parent_ids):
        clone = deepcopy(component)
        set_component_index(clone, index + 1)
        set_component_parent(clone, parent_id)

        clones.append(clone)

    return clones


def set_component_clones_ids(components: [TFPlanComponent]):
    for component in components:
        component.clones_ids = [s.id for s in components if s.id != component.id]


def set_component_index(component: TFPlanComponent, index: int):
    component.id = f'{component.id}_{index}'


def set_component_parent(component: TFPlanComponent, parent_id: str):
    component.parent_type = ParentType.COMPONENT
    component.parent = parent_id


def _find_parent_candidates_by_type(components: [], parent_type: str) -> []:
    return list(filter(lambda c: __extract_type(c.id) == parent_type, components))


def __extract_type(component_address: str) -> str:
    if component_address is not None and '.' in component_address:
        return component_address.split('.')[-2]


class HierarchyCalculator(Transformer):
    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)

        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=self.graph
        )

    def transform(self):
        clones = []

        for component in self.otm.components:
            parent_ids = self._calculate_component_parents(component)

            if not parent_ids:
                continue

            set_component_parent(component, parent_ids[0])

            if len(parent_ids) > 1:
                clones.extend(clone_component_by_parents(component, parent_ids[1:]))
                set_component_index(component, 0)
                set_component_clones_ids([component] + clones)

        self.otm.components.extend(clones)

    @abc.abstractmethod
    def _calculate_component_parents(self, component: TFPlanComponent) -> [str]:
        raise NotImplementedError

    def _find_parent_by_closest_relationship(self, component: TFPlanComponent, parent_candidates: []):
        return self.relationships_extractor.get_closest_resources(component, parent_candidates)

    def _get_parent_candidates(self, parent_types: []):
        parent_candidates = []

        for parent_type in parent_types:
            parent_candidates.extend(_find_parent_candidates_by_type(self.otm.components, parent_type))

        return parent_candidates
