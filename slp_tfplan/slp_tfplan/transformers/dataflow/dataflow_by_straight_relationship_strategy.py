from typing import List

from otm.otm.entity.dataflow import Dataflow
from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_creator import create_dataflow
from slp_tfplan.slp_tfplan.transformers.dataflow.dataflow_strategies import DataflowCreationStrategy


class DataflowByStraightRelationshipStrategy(DataflowCreationStrategy):
    def create_dataflows(self, **kwargs) -> List[Dataflow]:
        dataflows = []

        otm = kwargs['otm']
        relationships_extractor = kwargs['relationships_extractor']
        are_hierarchically_related = kwargs['are_hierarchically_related']

        for component in otm.components:
            for related_component in otm.components:
                if component == related_component:
                    continue

                if relationships_extractor.exist_valid_path(component.tf_resource_id,
                                                            related_component.tf_resource_id) \
                        and not are_hierarchically_related(component, related_component):
                    dataflows.append(create_dataflow(component, related_component))

        return dataflows
