from typing import Union, List

import networkx as nx
from networkx import DiGraph

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.load.tfplan_to_resource_dict import remove_name_prefix


class RelationshipsExtractor:

    def __init__(self, graph: DiGraph, mapped_resources_ids: [str]):
        self.graph = graph
        self.mapped_resources_ids = set(mapped_resources_ids)

        self.nodes_labels: dict = dict(self.graph.nodes(data='label'))
        self.labels_nodes: dict = {v: k for k, v in self.nodes_labels.items()}

    def get_closest_resources(self, source_component: TFPlanComponent, target_candidates: [TFPlanComponent]) -> [str]:
        linked_resources = []

        min_size = 0
        for target_candidate in target_candidates:
            path = self.__get_shortest_valid_path(
                source_component.tf_resource_id, target_candidate.tf_resource_id)

            if not path:
                continue

            path_size = len(path)
            if not linked_resources or path_size < min_size:
                min_size = path_size
                linked_resources = [target_candidate.id]
            elif path_size == min_size:
                linked_resources.append(target_candidate.id)

        return linked_resources

    def exist_valid_path(self, source_label: str, target_label: str) -> bool:
        return bool(self.__get_shortest_valid_path(source_label, target_label))

    def __get_shortest_valid_path(self, source_label: str, target_label: str) -> Union[List[str], None]:
        if not self.__are_equals_valid_graph_labels(source_label, target_label):
            return

        source_node = self.labels_nodes[source_label]
        target_node = self.labels_nodes[target_label]

        shortest_path = None
        if nx.has_path(self.graph, source_node, target_node):
            for path in nx.all_simple_paths(self.graph, source=source_node, target=target_node):
                if self.__is_straight_path(path):
                    if not shortest_path or len(shortest_path) > len(path):
                        shortest_path = path

        return shortest_path

    def __are_equals_valid_graph_labels(self, source_label: str, target_label: str) -> bool:
        return source_label != target_label \
                and source_label in self.labels_nodes \
                and target_label in self.labels_nodes

    def __is_straight_path(self, path: list) -> bool:
        return len(self.mapped_resources_ids & self.__nodes_to_labels(path[1:-1])) == 0

    def __nodes_to_labels(self, path: []) -> set:
        return set(filter(lambda x: x is not None, map(lambda p: remove_name_prefix(self.nodes_labels[p]), path)))
