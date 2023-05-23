import uuid
from abc import abstractmethod
from typing import List, Callable

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from otm.otm.entity.dataflow import Dataflow
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent


def create_dataflow(source_component: TFPlanComponent, target_component: TFPlanComponent, bidirectional: bool = False):
    return Dataflow(
        # TODO Generate deterministic ID
        dataflow_id=str(uuid.uuid4()),
        name=f'{source_component.name} to {target_component.name}',
        source_node=source_component.id,
        destination_node=target_component.id,
        bidirectional=bidirectional
    )


class DataflowCreationStrategy:
    # TODO Create documentation per strategy group

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'create_dataflows') and callable(subclass.process)
                or NotImplemented)

    @abstractmethod
    def create_dataflows(self,
                         otm: TFPlanOTM,
                         relationships_extractor: RelationshipsExtractor,
                         are_hierarchically_related: Callable) -> List[Dataflow]:
        raise NotImplementedError


class DataflowCreationStrategyContainer(DeclarativeContainer):
    strategies = providers.List()
