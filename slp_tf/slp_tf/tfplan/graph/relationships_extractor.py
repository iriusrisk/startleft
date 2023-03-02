from typing import Union

import networkx as nx
from networkx import DiGraph

from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanComponent


class RelationshipsExtractor:

    def __init__(self, graph: DiGraph, mapped_resources_ids: [str]):
        self.graph = graph
        self.mapped_resources_ids = set(mapped_resources_ids)

        self.nodes_labels: dict = dict(self.graph.nodes(data='label'))
        self.labels_nodes: dict = {v: k for k, v in self.nodes_labels.items()}

    def get_closest_resources(self, source_component: TfplanComponent, target_candidates: [TfplanComponent]) -> [str]:
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

    def __get_shortest_valid_path(self, source_label: str, target_label: str) -> list:
        source_node = self.labels_nodes[source_label]
        target_node = self.labels_nodes[target_label]

        shortest_path = None
        if self.__has_path(source_node, target_node):
            for path in nx.all_simple_paths(self.graph, source=source_node, target=target_node):
                if self.__is_straight_path(path):
                    if not shortest_path or len(shortest_path) > len(path):
                        shortest_path = path

        return shortest_path

    def __has_path(self, source_node: str, target_node: str) -> Union[int, None]:
        return source_node != target_node \
               and nx.has_path(self.graph, source_node, target_node)

    def __is_straight_path(self, path: list) -> bool:
        return len(self.mapped_resources_ids & self.__nodes_to_labels(path[1:-1])) == 0

    def __nodes_to_labels(self, path: []) -> set:
        return set(filter(lambda x: x is not None, map(lambda p: self.nodes_labels[p], path)))
