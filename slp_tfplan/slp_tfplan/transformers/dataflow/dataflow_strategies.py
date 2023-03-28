from abc import abstractmethod
from typing import List, Callable

from otm.otm.entity.dataflow import Dataflow
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM


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


