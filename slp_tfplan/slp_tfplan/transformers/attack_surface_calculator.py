import re
from enum import Enum
from typing import List

from dependency_injector.wiring import inject
from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.map.mapping import AttackSurface
from slp_tfplan.slp_tfplan.map.tfplan_mapper import trustzone_to_otm
from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent, SecurityGroupCIDR
from slp_tfplan.slp_tfplan.relationship.component_relationship_calculator import ComponentRelationshipCalculator, \
    ComponentRelationshipType
from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import create_dataflow
from slp_tfplan.slp_tfplan.util.tfplan import find_component_by_id, find_variable_name_by_value


def __is_ip_with_mask(ip: str) -> bool:
    return bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+$', ip))


def __is_public_ip(ip: str) -> bool:
    """
    Checks if the ip is a public ip
    it is not:
     * 10.0.0.0/8 => (10.0.0.0 – 10.255.255.255)
     * 172.16.0.0/12 => (172.16.0.0 – 172.31.255.255)
     * 192.168.0.0/16 => (192.168.0.0 – 192.168.255.255)
     * 169.254.0.0/16 => (169.254.0.0 – 169.254.255.255)
    :param ip:
    :return:
    """
    return not ip.startswith('10.') \
           and not re.match(r'^172\.(1[6-9]|2\d|3[0-1])\.', ip) \
           and not ip.startswith('192.168.') \
           and not ip.startswith('169.254.')


def __is_broadcast_ip(ip: str) -> bool:
    return ip.startswith('255.255.255.255')


def _is_valid_ip(ip: str) -> bool:
    """
    Checks if the ip is a valid ip and not a broadcast ip
    :param ip:
    :return:
    """
    return __is_ip_with_mask(ip) and __is_public_ip(ip) and not __is_broadcast_ip(ip)


def _create_client(client_id: str, client_name: str, attack_surface_mapping: AttackSurface) -> TFPlanComponent:
    return TFPlanComponent(
        component_id=client_id,
        name=client_name,
        component_type=attack_surface_mapping.client,
        parent=attack_surface_mapping.trustzone.type,
        parent_type=ParentType.TRUST_ZONE,
        tags=[]
    )


def _generate_protocol_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    protocol = "all" if security_group_cidr.protocol == "-1" else security_group_cidr.protocol
    from_port = "N/A" if security_group_cidr.from_port is None else security_group_cidr.from_port
    to_port = "N/A" if security_group_cidr.to_port is None else security_group_cidr.to_port
    return ["protocol: {}".format(protocol), "from_port: {} to_port: {}".format(from_port, to_port)]


def _generate_cidr_blocks_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    return ["ip: {}".format(ip) for ip in security_group_cidr.cidr_blocks if _is_valid_ip(ip)]


def _generate_security_group_cidr_tags(security_group_cidr: SecurityGroupCIDR) -> List[str]:
    result = []
    result.extend(_generate_protocol_tags(security_group_cidr))
    result.extend(_generate_cidr_blocks_tags(security_group_cidr))

    return result


def _generate_client_id(security_group: SecurityGroupCIDR):
    valids_ips = ", ".join(sorted(security_group.cidr_blocks))
    return deterministic_uuid(valids_ips)


class DataflowDirection(Enum):
    INGRESS = 'ingress'
    EGRESS = 'egress'


class AttackSurfaceCalculator:
    """
    Calculate the attack surface of the infrastructure
    This attack surface is calculated based on the security groups and the components that are in the security groups
    Currently, it calculates the attack surface based on the ingres rules of the security groups
    """

    @inject
    def __init__(self, otm: TFPlanOTM, graph: DiGraph, attack_surface_mapping: AttackSurface):
        self.otm = otm
        self.graph = graph
        self.attack_surface_mapping: AttackSurface = attack_surface_mapping
        self.component_relationship_calculator = ComponentRelationshipCalculator(self.otm)
        self.relationships_extractor = RelationshipsExtractor(
            mapped_resources_ids=self.otm.mapped_resources_ids,
            graph=graph)
        self.clients: List[TFPlanComponent] = []
        self.dataflows: List[Dataflow] = []

    def transform(self):
        """
        Calculate the attack surface of the infrastructure
        Add the clients, trustzones and dataflows to the otm indicating the inbound attack surface
        :return:
        """
        if not self.attack_surface_mapping.client:
            return

        self.calculate_clients_and_dataflows()
        self.otm.components.extend(self.clients)
        self.otm.dataflows.extend(self.__remove_parent_dataflows())
        self.add_attack_surface_trustzone()

    def calculate_clients_and_dataflows(self):
        components_in_sgs = ComponentsAndSGsMatcher(self.otm, self.relationships_extractor).match()
        for sg_id in components_in_sgs:
            sg = self.__get_security_group_by_id(sg_id)
            components = components_in_sgs[sg_id]
            self.__generate_dataflows(sg.ingress_cidr, components, DataflowDirection.INGRESS)

    def __get_security_group_by_id(self, sg_id: str):
        return next(filter(lambda e: e.id == sg_id, self.otm.security_groups))

    def __generate_dataflows(self, security_group_cidr: List[SecurityGroupCIDR], components: List[TFPlanComponent],
                             direction: DataflowDirection):
        for security_group in security_group_cidr or []:
            self.__generate_dataflow_by_cidr_block(components, direction, security_group)

    def __generate_dataflow_by_cidr_block(self, components, direction, security_group: SecurityGroupCIDR):
        no_valids_ips = not any(filter(lambda ip: _is_valid_ip(ip), security_group.cidr_blocks))
        if no_valids_ips:
            return

        client_component = self.__generate_client(security_group)
        for component in components:
            flow = (client_component, component) if direction == DataflowDirection.INGRESS \
                else (component, client_component)
            self.dataflows.append(create_dataflow(
                flow[0], flow[1], name=security_group.description,
                tags=_generate_security_group_cidr_tags(security_group)))

    def __generate_client_name(self, security_group: SecurityGroupCIDR):
        var_name = find_variable_name_by_value(self.otm.variables, security_group.cidr_blocks)
        if var_name:
            return var_name

        valids_ips = list(filter(lambda ip: _is_valid_ip(ip), security_group.cidr_blocks))
        if len(valids_ips) == 1:
            return valids_ips[0]

        if security_group.description:
            return security_group.description

        return self.attack_surface_mapping.client

    def __generate_client(self, security_group: SecurityGroupCIDR):
        client_id = _generate_client_id(security_group)
        client_name = self.__generate_client_name(security_group)
        if not self.__exists_ip_as_client(client_id):
            self.clients.append(_create_client(client_id, client_name, self.attack_surface_mapping))
        return self.__get_ip_as_client(client_id)

    def __get_ip_as_client(self, ip: str) -> TFPlanComponent:
        return next(filter(lambda c: c.id == ip, self.clients))

    def __exists_ip_as_client(self, ip: str) -> bool:
        return any(filter(lambda c: c.id == ip, self.clients))

    def __exists_component_with_parent(self, parent: str) -> bool:
        return any(filter(lambda c: c.parent == parent, self.otm.components))

    def __exists_trustzone_with_type(self, trustzone_type: str) -> bool:
        return any(filter(lambda t: t.type == trustzone_type, self.otm.trustzones))

    def add_attack_surface_trustzone(self):
        if self.__exists_component_with_parent(self.attack_surface_mapping.trustzone.type) and \
                not self.__exists_trustzone_with_type(self.attack_surface_mapping.trustzone.type):
            self.otm.trustzones.append(trustzone_to_otm(self.attack_surface_mapping.trustzone))

    def __remove_parent_dataflows(self) -> List[Dataflow]:
        """
        Returns a list of dataflows where:
            If component (A) has a dataflow to (B, C) and B is Ancestor (parent) of C, then the dataflow to B is removed
        """
        result: List[Dataflow] = []
        for df in self.dataflows:
            if not self.__is_dataflow_parent_of_any_dataflow(df, self.dataflows):
                result.append(df)
        return result

    def __is_dataflow_parent_of_any_dataflow(self, parent_df, dataflows: List[Dataflow]):
        parent_source_node_component = find_component_by_id(parent_df.source_node, self.otm.components)
        parent_destination_node_component = find_component_by_id(parent_df.destination_node, self.otm.components)
        parent_name = parent_df.name

        for child_df in dataflows:
            if self.__is_parent_dataflow_with_same_name(
                    parent_source_node_component, parent_destination_node_component, parent_name, child_df):
                return True
        return False

    def __is_parent_dataflow_with_same_name(self,
                                            parent_source_node_component: TFPlanComponent,
                                            parent_destination_node_component: TFPlanComponent,
                                            parent_name: str,
                                            child_df: Dataflow) -> bool:

        is_parent_relationships = {ComponentRelationshipType.SAME, ComponentRelationshipType.ANCESTOR}
        child_source_node_component = find_component_by_id(child_df.source_node, self.otm.components)
        child_destination_node_component = find_component_by_id(child_df.destination_node, self.otm.components)
        child_name = child_df.name

        relations = {
            self.component_relationship_calculator.get_relationship(
                parent_source_node_component, child_source_node_component),
            self.component_relationship_calculator.get_relationship(
                parent_destination_node_component, child_destination_node_component)
        }
        return relations == is_parent_relationships and parent_name == child_name
