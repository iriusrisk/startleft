import itertools
from typing import List, Dict

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.otm import OTM
from sl_util.sl_util.iterations_utils import remove_from_list
from slp_tf.slp_tf.tfplan.tfplan_component import TfplanComponent
from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer


def _merge_component_configurations(otm_components: List[TfplanComponent]) -> {}:
    merge_configuration = {}
    for component in otm_components:
        merge_configuration = {
            **merge_configuration, **component.configuration
        }
    return merge_configuration


def _find_equals_dataflows(dataflow, dataflows):
    equals_dataflows = []
    for df in dataflows:
        if _is_equals_dataflow(dataflow, df):
            equals_dataflows.append(df)

    return equals_dataflows


def _is_equals_dataflow(dataflow_1, dataflow_2):
    is_same_flow = (dataflow_1.source_node == dataflow_2.source_node
                    and dataflow_1.destination_node == dataflow_2.destination_node)

    is_reverse_bidirectional_flow = (dataflow_1.bidirectional or dataflow_2.bidirectional) \
                                    and dataflow_1.source_node == dataflow_2.destination_node \
                                    and dataflow_1.destination_node == dataflow_2.source_node

    return is_same_flow or is_reverse_bidirectional_flow


def _merge_dataflow(origin_dataflow: Dataflow, dataflows: List[Dataflow]):
    if len(dataflows) > 0:
        for df in dataflows:
            if origin_dataflow.tags is None:
                origin_dataflow.tags = df.tags
            else:
                origin_dataflow.tags.extend(df.tags or [])
                origin_dataflow.tags = list(set(origin_dataflow.tags))

            if origin_dataflow.attributes is None:
                origin_dataflow.attributes = df.attributes
            else:
                origin_dataflow.attributes.extend(df.attributes or [])
                origin_dataflow.attributes = list(set(origin_dataflow.attributes))

            if (origin_dataflow.source_node == df.destination_node
                and origin_dataflow.destination_node == df.source_node) \
                    or df.bidirectional:
                origin_dataflow.bidirectional = True

    return origin_dataflow


class TfplanSingletonTransformer(TfplanTransformer):

    def __init__(self, otm: OTM):
        super().__init__(otm)
        self.otm_components = self.otm.components
        self.otm_dataflows = self.otm.dataflows
        self.singleton_component_relations: Dict[str, TfplanComponent] = {}
        self.__populate_singleton_component_relations()

    def __populate_singleton_component_relations(self):
        for component in self.otm_components:
            if component.is_singleton:
                sibling_components = self.__find_siblings_components(component.type, component.parent)
                if len(sibling_components) > 1:
                    singleton_component = self.__get_singleton(sibling_components)
                    self.singleton_component_relations[component.id] = singleton_component

    def __find_siblings_components(self, component_type: str, parent_id: str):
        """
        Returns all the component marked as singleton with the given type and parent identifier
        :param component_type: Type of the component
        :param parent_id:  Identifier of the parent component
        :return: A list with all the related components
        """
        found_components = []
        for component in self.otm_components:
            if (component.is_singleton
                    and component.type == component_type
                    and component.parent == parent_id):
                found_components.append(component)

        return found_components

    def __get_singleton(self, otm_components: List[TfplanComponent]):
        tags = list(set(itertools.chain.from_iterable([c.tags or [] for c in otm_components])))
        configuration = _merge_component_configurations(otm_components)
        component_id = otm_components[0].id
        return self.singleton_component_relations.get(component_id, TfplanComponent(
            component_id=component_id,
            name=f"{otm_components[0].type} (grouped)",
            component_type=otm_components[0].type,
            parent=otm_components[0].parent,
            parent_type=otm_components[0].parent_type,
            tags=tags,
            configuration=configuration
        ))

    def __get_unique_singleton_components(self):
        index = []
        unique_singleton_components = []
        for value in self.singleton_component_relations.values():
            if value.id not in index:
                index.append(value.id)
                unique_singleton_components.append(value)
        return unique_singleton_components

    def transform(self):
        self.__transform_singleton_components()
        self.__transform_singleton_dataflows()

    def __transform_singleton_components(self):
        # remove all singletons
        remove_from_list(
            self.otm_components, lambda component: component.id in self.singleton_component_relations
        )
        # add all unique singletons
        self.otm_components.extend(self.__get_unique_singleton_components())

    def __transform_singleton_dataflows(self):
        if self.otm_dataflows:
            self.__unify_dataflows_by_singleton_relationship()
            self.otm.dataflows = self.__get_unique_singleton_dataflows()

    def __unify_dataflows_by_singleton_relationship(self):
        for dataflow in self.otm_dataflows:
            if dataflow.source_node in self.singleton_component_relations:
                dataflow.source_node = self.singleton_component_relations[dataflow.source_node].id

            if dataflow.destination_node in self.singleton_component_relations:
                dataflow.destination_node = self.singleton_component_relations[dataflow.destination_node].id

    def __get_unique_singleton_dataflows(self):
        unique_singleton_dataflows = []
        repeated_dataflows = []

        for index, dataflow in enumerate(self.otm_dataflows):
            if any(dataflow.id == repeated_df.id for repeated_df in repeated_dataflows):
                continue

            if index == len(self.otm_dataflows):
                unique_singleton_dataflows.append(dataflow)
                continue

            equals_dataflows = _find_equals_dataflows(dataflow, self.otm_dataflows[index + 1:])
            repeated_dataflows.extend(equals_dataflows)
            unique_singleton_dataflows.append(_merge_dataflow(dataflow, equals_dataflows))

        return unique_singleton_dataflows
