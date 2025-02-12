from abc import abstractmethod
from typing import List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from otm.otm.entity.dataflow import Dataflow
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent


def __create_directed_id(source_component_id: str, target_component_id: str):
    return deterministic_uuid(f'{source_component_id}-{target_component_id}')


def __create_undirected_id(source_component_id: str, target_component_id: str):
    components = [source_component_id, target_component_id]
    components.sort()
    return deterministic_uuid(f'{components[0]}-{components[1]}-bidirectional')


def __create_deterministic_id(source_component_id: str, target_component_id: str, bidirectional: bool):
    return __create_undirected_id(source_component_id, target_component_id) if bidirectional \
        else __create_directed_id(source_component_id, target_component_id)


def __generate_default_dataflow_name(source_component: TFPlanComponent, target_component: TFPlanComponent,
                                     bidirectional: bool):
    return f'{source_component.name} to {target_component.name} (bidirectional)' \
        if bidirectional else f'{source_component.name} to {target_component.name}'


def create_dataflow(source_component: TFPlanComponent, target_component: TFPlanComponent,
                    name: str = None, bidirectional: bool = False, tags=None):
    dataflow_id = __create_deterministic_id(source_component.id, target_component.id, bidirectional)
    if not name:
        name = __generate_default_dataflow_name(source_component, target_component, bidirectional)

    return Dataflow(
        dataflow_id=dataflow_id,
        name=name,
        source_node=source_component.id,
        destination_node=target_component.id,
        bidirectional=bidirectional,
        tags=tags
    )


class DataflowCreationStrategy:

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'create_dataflows') and callable(subclass.process)
                or NotImplemented)

    @abstractmethod
    def create_dataflows(self,
                         otm: TFPlanOTM,
                         relationships_extractor: RelationshipsExtractor) -> List[Dataflow]:
        """
        Common method to build dataflows based on a tfplan OTM and a tfgraph.
        These dataflows can be found in different ways (using the graph, using security groups, etc.).
        Each implementation defines one specific logic to create dataflows.
        :param otm: `TFPlanOTM` object with all the components mapped for a given tfplan.
        :param relationships_extractor: object with methods to find relationships in the tfgraph.
        two components.
        :return: the list of calculated `Dataflow`.
        """
        raise NotImplementedError


class DataflowCreationStrategyContainer(DeclarativeContainer):
    """
    Container with instances for each `DataflowCreationStrategy` implementation to be injected using
    dependency-injector (see https://python-dependency-injector.ets-labs.org/).
    """

    strategies = providers.List()
