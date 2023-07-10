from typing import List, Union, Dict

from dependency_injector.wiring import inject
from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from sl_util.sl_util.ip_utils import is_public_ip, is_ip_with_mask, is_broadcast_ip
from sl_util.sl_util.iterations_utils import compare_unordered_list_or_string
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.map.mapping import AttackSurface
from slp_tfplan.slp_tfplan.map.tfplan_mapper import trustzone_to_otm
from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent, SecurityGroupCIDR, \
    SecurityGroupCIDRType
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator, \
    ComponentRelationshipType
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import create_dataflow


def _is_valid_cidr(cidr: str) -> bool:
    return is_ip_with_mask(cidr) and is_public_ip(cidr) and not is_broadcast_ip(cidr)


def _get_variable_name_by_value(value: Union[list, str], variables: Dict) -> str:
    for k, v in variables.items():
        if compare_unordered_list_or_string(v, value):
            return k


def _create_client(client_id: str, variables: Dict, security_group_cidr: SecurityGroupCIDR,
                   attack_surface_configuration: AttackSurface) -> TFPlanComponent:
    return TFPlanComponent(
        component_id=client_id,
        name=_generate_client_name(security_group_cidr, variables, attack_surface_configuration.client),
        component_type=attack_surface_configuration.client,
        parent=attack_surface_configuration.trustzone.type,
        parent_type=ParentType.TRUST_ZONE,
        tags=[]
    )


def _generate_client_id(security_group_cidr: SecurityGroupCIDR):
    if security_group_cidr.cidr_blocks:
        valids_ips = ", ".join(sorted(security_group_cidr.cidr_blocks))
        return deterministic_uuid(valids_ips)


def _generate_client_name(security_group_cidr: SecurityGroupCIDR, variables: Dict, attack_surface_client: str):
    cidr_var_name = _get_variable_name_by_value(security_group_cidr.cidr_blocks, variables)
    if cidr_var_name:
        return cidr_var_name

    valids_ips = list(filter(_is_valid_cidr, security_group_cidr.cidr_blocks))
    if len(valids_ips) == 1:
        return valids_ips[0]

    if security_group_cidr.description:
        return security_group_cidr.description

    return attack_surface_client


def _generate_protocol_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    protocol = "all" if security_group_cidr.protocol == "-1" else security_group_cidr.protocol
    from_port = "N/A" if security_group_cidr.from_port is None else security_group_cidr.from_port
    to_port = "N/A" if security_group_cidr.to_port is None else security_group_cidr.to_port
    return ["protocol: {}".format(protocol), "from_port: {} to_port: {}".format(from_port, to_port)]


def _generate_cidr_blocks_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    return ["ip: {}".format(ip) for ip in security_group_cidr.cidr_blocks if _is_valid_cidr(ip)]


def _generate_security_group_cidr_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    result = []
    result.extend(_generate_protocol_tags(security_group_cidr))
    result.extend(_generate_cidr_blocks_tags(security_group_cidr))

    return result


class AttackSurfaceCalculator:
    """
    Calculate the attack surface of the infrastructure
    This attack surface is calculated based on the security groups and the components that are in the security groups
    Currently, it calculates the attack surface based on the ingres rules of the security groups
    """

    @inject
    def __init__(self, otm: TFPlanOTM, graph: DiGraph, attack_surface_configuration: AttackSurface):
        self.otm = otm
        self.graph = graph
        self.attack_surface_configuration: AttackSurface = attack_surface_configuration

        self._clients: List[TFPlanComponent] = []
        self._dataflows: List[Dataflow] = []

        _relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=graph)
        self._components_and_sgs_matcher = ComponentsAndSGsMatcher(self.otm, _relationships_extractor)
        self._component_relationship_calculator = ComponentRelationshipCalculator(self.otm)

    def transform(self):
        """
        Calculate the attack surface of the infrastructure
        Add the clients, trustzones and dataflows to the otm indicating the inbound attack surface
        :return:
        """
        if not self.attack_surface_configuration.client:
            return

        self.add_clients_and_dataflows()
        self.add_attack_surface_trustzone()

    def add_clients_and_dataflows(self):
        components_in_sgs = self._components_and_sgs_matcher.match()
        for sg_id in components_in_sgs:
            self.__generate_dataflows(security_group_cidrs=self.otm.get_security_group_by_id(sg_id).ingress_cidr,
                                      components=components_in_sgs[sg_id])

        self.otm.components.extend(self._clients)
        self.otm.dataflows.extend(filter(lambda df: not self.__is_parent_dataflow(df), self._dataflows))

    def __generate_dataflows(self, security_group_cidrs: List[SecurityGroupCIDR], components: List[TFPlanComponent]):
        for security_group_cidr in security_group_cidrs or []:
            if any(filter(_is_valid_cidr, security_group_cidr.cidr_blocks)):
                self.__generate_dataflow_by_cidr_block(components, security_group_cidr)

    def __generate_dataflow_by_cidr_block(self, components: List[TFPlanComponent], security_group: SecurityGroupCIDR):
        client_component = self.__generate_client(security_group)
        for component in components:
            flow = (client_component, component) if security_group.type == SecurityGroupCIDRType.INGRESS \
                else (component, client_component)
            self._dataflows.append(create_dataflow(*flow,
                                                   name=security_group.description,
                                                   tags=_generate_security_group_cidr_tags(security_group)))

    def __generate_client(self, security_group_cidr: SecurityGroupCIDR):
        client_id = _generate_client_id(security_group_cidr)

        if not self.__exists_client_by_id(client_id):
            self._clients.append(
                _create_client(client_id, self.otm.variables, security_group_cidr, self.attack_surface_configuration))

        return self.__get_client_by_id(client_id)

    def __get_client_by_id(self, client_id: str) -> TFPlanComponent:
        return next(filter(lambda c: c.id == client_id, self._clients), None)

    def __exists_client_by_id(self, client_id: str) -> bool:
        return any(filter(lambda c: c.id == client_id, self._clients))

    def __is_parent_dataflow(self, dataflow: Dataflow):
        """
        It checks if a dataflow is parent of another dataflow.
        If component (A) has a dataflow to (B, C) and B is Ancestor (parent) of C,
        then the dataflow to B is parent of the dataflow to C.
        Returns:
             True if the dataflow is a parent of other dataflow
             False otherwise
        """
        parent_source_node_component = self.otm.get_component_by_id(dataflow.source_node)
        parent_destination_node_component = self.otm.get_component_by_id(dataflow.destination_node)
        parent_name = dataflow.name

        for df_to_child in self._dataflows:
            if self.__is_same_dataflow_to_parent(
                    parent_source_node_component, parent_destination_node_component, parent_name, df_to_child):
                return True
        return False

    def __is_same_dataflow_to_parent(self,
                                     parent_source_node_component: TFPlanComponent,
                                     parent_destination_node_component: TFPlanComponent,
                                     parent_name: str,
                                     df_to_child: Dataflow) -> bool:
        same_or_ancestor_relationships = {ComponentRelationshipType.SAME, ComponentRelationshipType.ANCESTOR}
        child_source_node_component = self.otm.get_component_by_id(df_to_child.source_node)
        child_destination_node_component = self.otm.get_component_by_id(df_to_child.destination_node)
        child_name = df_to_child.name

        relations = {
            self._component_relationship_calculator.get_relationship(
                parent_source_node_component, child_source_node_component),
            self._component_relationship_calculator.get_relationship(
                parent_destination_node_component, child_destination_node_component)
        }
        return parent_name == child_name and relations == same_or_ancestor_relationships

    def add_attack_surface_trustzone(self):
        if self.otm.exists_component_with_parent(self.attack_surface_configuration.trustzone.type) and \
                not self.otm.exists_trustzone_with_type(self.attack_surface_configuration.trustzone.type):
            self.otm.trustzones.append(trustzone_to_otm(self.attack_surface_configuration.trustzone))
