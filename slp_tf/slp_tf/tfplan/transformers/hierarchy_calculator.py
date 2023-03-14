import abc
from copy import deepcopy

from networkx import DiGraph

from otm.otm.entity.parent_type import ParentType
from slp_tf.slp_tf.tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanComponent, TfplanOTM
from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer


def replicate_component_by_parents(component: TfplanComponent, parent_ids: [str]) -> [{}]:
    replicated_components = []

    for index, parent_id in enumerate(parent_ids):
        replicated_component = deepcopy(component)
        set_component_index(replicated_component, index + 1)
        set_component_parent(replicated_component, parent_id)

        replicated_components.append(replicated_component)

    return replicated_components


def set_component_clones_ids(components: [TfplanComponent]):
    for component in components:
        component.clones_ids = [s.id for s in components if s.id != component.id]


def set_component_index(component: TfplanComponent, index: int):
    component.id = f'{component.id}_{index}'


def set_component_parent(component: TfplanComponent, parent_id: str):
    component.parent_type = ParentType.COMPONENT
    component.parent = parent_id


def _find_parent_candidates_by_type(components: [], parent_type: str) -> []:
    return list(filter(lambda c: __extract_type(c.id) == parent_type, components))


def __extract_type(component_address: str) -> str:
    if component_address is not None and '.' in component_address:
        return component_address.split('.')[-2]


class HierarchyCalculator(TfplanTransformer):
    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)

        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=self.graph
        )

    def transform(self):
        replicated_components = []

        for component in self.otm.components:
            parent_ids = self._calculate_component_parents(component)

            if not parent_ids:
                continue

            set_component_parent(component, parent_ids[0])

            if len(parent_ids) > 1:
                replicated_components.extend(replicate_component_by_parents(component, parent_ids[1:]))
                set_component_index(component, 0)
                set_component_clones_ids([component] + replicated_components)

        self.otm.components.extend(replicated_components)

    @abc.abstractmethod
    def _calculate_component_parents(self, component: TfplanComponent) -> [str]:
        raise NotImplementedError

    def _find_parent_by_closest_relationship(self, component: TfplanComponent, parent_candidates: []):
        return self.relationships_extractor.get_closest_resources(component, parent_candidates)

    def _get_parent_candidates(self, parent_types: []):
        parent_candidates = []

        for parent_type in parent_types:
            parent_candidates.extend(_find_parent_candidates_by_type(self.otm.components, parent_type))

        return parent_candidates
