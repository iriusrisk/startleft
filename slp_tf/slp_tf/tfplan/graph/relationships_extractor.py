from typing import Union

import networkx as nx
from networkx import DiGraph

from slp_tf.slp_tf.tfplan.tfplan_component import TfplanComponent


class RelationshipsExtractor:

    def __init__(self, graph: DiGraph, mapped_resources_ids: [str]):
        self.graph = graph
        self.mapped_resources_ids = set(mapped_resources_ids)

        self.nodes_labels: dict = dict(self.graph.nodes(data='label'))
        self.labels_nodes: dict = {v: k for k, v in self.nodes_labels.items()}

    def get_closest_resources(self, source_component: TfplanComponent, target_candidates: [TfplanComponent]) -> [str]:
        liked_resources = []

        min_size = 0
        for target_candidate in target_candidates:
            path_size = self.__get_shortest_straight_path_size(
                source_component.tf_resource_id, target_candidate.tf_resource_id)

            if not path_size:
                continue

            if not liked_resources or path_size < min_size:
                min_size = path_size
                liked_resources = [target_candidate.id]
            elif path_size == min_size:
                liked_resources.append(target_candidate.id)

        return liked_resources

    def __get_shortest_straight_path_size(self, source_label: str, target_label: str) -> Union[int, None]:
        if source_label == target_label:
            return

        source_node = self.labels_nodes[source_label]
        target_node = self.labels_nodes[target_label]

        if nx.has_path(self.graph, source_node, target_node):
            shortest_path = nx.shortest_path(self.graph, source_node, target_node)
            if self.__is_straight_path(shortest_path):
                return len(shortest_path)

    def __is_straight_path(self, path: list) -> bool:
        return len(self.mapped_resources_ids & self.__nodes_to_labels(path[1:-1])) == 0

    def __nodes_to_labels(self, path: []) -> set:
        return set(map(lambda p: self.nodes_labels[p], path))
