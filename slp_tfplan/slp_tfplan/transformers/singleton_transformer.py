import itertools
from typing import List, Dict

from otm.otm.entity.dataflow import Dataflow
from sl_util.sl_util.iterations_utils import remove_from_list
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM
from slp_tfplan.slp_tfplan.transformers.transformer import Transformer
from slp_tfplan.slp_tfplan.util.tfplan import find_component_by_id


def _merge_component_configurations(otm_components: List[TFPlanComponent]) -> Dict:
    merge_configuration = {}
    for component in otm_components:
        merge_configuration = {
            **merge_configuration, **component.configuration
        }
    return merge_configuration


def _find_equivalent_dataflows(dataflow: Dataflow, dataflows: List[Dataflow]) -> List[Dataflow]:
    equivalent_dataflows = []
    for df in dataflows:
        if _are_equivalent_dataflows(dataflow, df):
            equivalent_dataflows.append(df)

    return equivalent_dataflows


def _are_equivalent_dataflows(dataflow_1: Dataflow, dataflow_2: Dataflow) -> bool:
    is_same_dataflow = (dataflow_1.source_node == dataflow_2.source_node
                    and dataflow_1.destination_node == dataflow_2.destination_node)

    is_reverse_bidirectional_dataflow = (dataflow_1.bidirectional or dataflow_2.bidirectional) \
                                    and dataflow_1.source_node == dataflow_2.destination_node \
                                    and dataflow_1.destination_node == dataflow_2.source_node

    return is_same_dataflow or is_reverse_bidirectional_dataflow


def _merge_dataflows(origin_dataflow: Dataflow, dataflows: List[Dataflow]) -> Dataflow:
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


def _build_singleton_component(otm_components: List[TFPlanComponent]) -> TFPlanComponent:
    tags = list(set(itertools.chain.from_iterable([c.tags or [] for c in otm_components])))
    configuration = _merge_component_configurations(otm_components)
    component_id = otm_components[0].id
    return TFPlanComponent(
        component_id=component_id,
        name=f"{otm_components[0].type} (grouped)",
        component_type=otm_components[0].type,
        parent=otm_components[0].parent,
        parent_type=otm_components[0].parent_type,
        tags=tags,
        configuration=configuration
    )


class SingletonTransformer(Transformer):

    def __init__(self, otm: TFPlanOTM):
        super().__init__(otm)
        self.otm_components = self.otm.components
        self.otm_dataflows = self.otm.dataflows

        self.singleton_component_relations: Dict[str, TFPlanComponent] = {}

    def transform(self):
        self.__populate_singleton_component_relations()
        self.__transform_singleton_components()
        self.__transform_singleton_dataflows()

    def __populate_singleton_component_relations(self):
        for component in self.otm_components:
            if component.is_singleton and self.__is_not_parent(component):
                sibling_components = self.__find_siblings_components(component.type, component.parent)
                if len(sibling_components) > 1:
                    self.singleton_component_relations[component.id] = \
                        self.singleton_component_relations.get(sibling_components[0].id) \
                        or _build_singleton_component(sibling_components)

    def __is_not_parent(self, component: TFPlanComponent):
        return not any(c.parent == component.id for c in self.otm_components)

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
                    and self.__is_not_parent(component)
                    and component.type == component_type
                    and component.parent == parent_id):
                found_components.append(component)

        return found_components

    def __transform_singleton_components(self):
        self.__remove_all_singletons()
        self.otm_components.extend(self.__get_unique_singleton_components())

    def __remove_all_singletons(self):
        remove_from_list(
            self.otm_components, filter_function=lambda component: component.id in self.singleton_component_relations
        )

    def __get_unique_singleton_components(self):
        index = []
        unique_singleton_components = []
        for value in self.singleton_component_relations.values():
            if value.id not in index:
                index.append(value.id)
                unique_singleton_components.append(value)
        return unique_singleton_components

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
            if dataflow.source_node == dataflow.destination_node:
                continue

            if any(dataflow.id == repeated_df.id for repeated_df in repeated_dataflows):
                continue

            if index == len(self.otm_dataflows):
                unique_singleton_dataflows.append(dataflow)
                continue

            source_component = find_component_by_id(dataflow.source_node, self.otm_components)
            destination_component = find_component_by_id(dataflow.destination_node, self.otm_components)
            if not source_component.is_singleton and not destination_component.is_singleton:
                unique_singleton_dataflows.append(dataflow)
                continue

            equivalent_dataflows = _find_equivalent_dataflows(dataflow, self.otm_dataflows[index + 1:])
            repeated_dataflows.extend(equivalent_dataflows)
            unique_singleton_dataflows.append(_merge_dataflows(dataflow, equivalent_dataflows))

        return unique_singleton_dataflows
