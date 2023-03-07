import uuid

from networkx import DiGraph
from typing import Dict, List

from otm.otm.entity.dataflow import Dataflow
from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanOTM, TfplanComponent, TfplanSecurityGroup
from slp_tf.slp_tf.tfplan.graph.relationships_extractor import RelationshipsExtractor


def have_components_relationship(first: TfplanComponent, second: TfplanComponent):
    return first.id == second.id or first.parent == second.id or second.parent == first.id


def create_dataflows_among_components(
        source_components: List[TfplanComponent], target_components: List[TfplanComponent]):
    dataflows = []

    for source_component in source_components:
        for target_component in target_components:
            if not have_components_relationship(source_component, target_component):
                dataflows.append(create_dataflow(source_component, target_component))

    return dataflows


def create_dataflow(source_component: TfplanComponent, target_component: TfplanComponent, bidirectional: bool = False):
    return Dataflow(
        # FIXME Generate deterministic ID
        dataflow_id=str(uuid.uuid4()),
        name=f'{source_component.name} to {target_component.name}',
        source_node=source_component.id,
        destination_node=target_component.id,
        bidirectional=bidirectional
    )


class TfplanDataflowCreator(TfplanTransformer):

    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)

        self.components: [TfplanComponent] = otm.components
        self.security_groups: [TfplanSecurityGroup] = otm.security_groups
        self.dataflows: [Dataflow] = otm.dataflows

        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=
            [component.id for component in self.otm.components] +
            [sg.id for sg in self.otm.security_groups] +
            [lt.id for lt in self.otm.launch_templates],
            graph=self.graph
        )

        self.components_sgs: Dict[str, List[TfplanComponent]] = {}
        self.sgs_relationships: Dict[str, List[str]] = {}

    def transform(self):
        self.components_sgs = self.__match_components_and_sgs()
        if not self.components_sgs:
            return

        self.sgs_relationships = self.__find_sgs_relationships()
        if not self.sgs_relationships:
            return

        self.dataflows.extend(self.__create_dataflows_from_sgs())

    def __create_dataflows_from_sgs(self):
        dataflows = []

        for source_sg, target_sgs in self.sgs_relationships.items():
            if source_sg not in self.components_sgs:
                continue

            for target_sg in target_sgs:
                if target_sg in self.components_sgs:
                    dataflows.extend(create_dataflows_among_components(
                        self.components_sgs[source_sg], self.components_sgs[target_sg]))

        return dataflows

    def __match_components_and_sgs(self) -> Dict[str, List[TfplanComponent]]:
        components_in_sgs: Dict[str, List[TfplanComponent]] = {}

        for security_group in self.security_groups:
            components_in_sg = []
            for component in self.components:
                if self.__are_components_related_by_graph(component, security_group) or \
                        self.__are_related_by_launch_template(component, security_group):
                    components_in_sg.append(component)

            if components_in_sg:
                components_in_sgs[security_group.id] = components_in_sg

        return components_in_sgs

    def __are_components_related_by_graph(self, component: TfplanComponent, security_group: TfplanSecurityGroup) -> bool:
        return self.relationships_extractor.exist_valid_path(component.tf_resource_id, security_group.id) or \
                    self.relationships_extractor.exist_valid_path(security_group.id, component.tf_resource_id)

    def __are_related_by_launch_template(self, component: TfplanComponent, security_group: TfplanSecurityGroup) -> bool:
        for launch_template in self.otm.launch_templates:
            if not self.relationships_extractor.exist_valid_path(component.tf_resource_id, launch_template.id):
                continue
            if security_group.id in launch_template.security_groups_ids:
                return True

    def __find_sgs_relationships(self) -> Dict[str, List[str]]:
        sgs_relationships: Dict[str, List[str]] = {}

        for source_sg in self.security_groups:
            sg_relationships = []

            for target_sg in self.security_groups:
                if source_sg.id == target_sg.id:
                    continue

                if self.__are_sgs_related_by_configuration(source_sg, target_sg) or \
                        self.__are_sgs_related_by_graph(source_sg, target_sg):
                    sg_relationships.append(target_sg.id)

            if sg_relationships:
                sgs_relationships[source_sg.id] = list(set(sg_relationships))

        return sgs_relationships

    def __are_sgs_related_by_configuration(self, source_sg: TfplanSecurityGroup, target_sg: TfplanSecurityGroup) -> bool:
        return source_sg.id in target_sg.ingress_sgs or target_sg.id in source_sg.egress_sgs

    def __are_sgs_related_by_graph(self, source_sg: TfplanSecurityGroup, target_sg: TfplanSecurityGroup) -> bool:
        return self.relationships_extractor.exist_valid_path(target_sg.id, source_sg.id)


