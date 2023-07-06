from typing import List, Dict, Union

from slp_tfplan.slp_tfplan.load.resource_data_extractors import security_group_id_from_rule, \
    description_from_rule, protocol_from_rule, from_port_from_rule, to_port_from_rule, cidr_blocks_from_rule, \
    cidr_from_type_property, source_security_group_id_from_rule, \
    security_group_rule_type, security_groups_ids_from_type_property
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup, TFPlanOTM, SecurityGroupCIDR, \
    SecurityGroupCIDRType

SECURITY_GROUPS_TYPES = ['aws_security_group']
SECURITY_GROUP_RULE_TYPES = ['aws_security_group_rule']


def _get_security_group_rules(resources: List[Dict]) -> List[Dict[str, str]]:
    sg_rules = list(filter(lambda r: r['resource_type'] in SECURITY_GROUP_RULE_TYPES, resources))
    if not sg_rules:
        return []

    return list(map(lambda sg_rule:
                    {'security_group_id': security_group_id_from_rule(sg_rule),
                     'description': description_from_rule(sg_rule),
                     'protocol': protocol_from_rule(sg_rule),
                     'from_port': from_port_from_rule(sg_rule),
                     'to_port': to_port_from_rule(sg_rule),
                     'cidr_blocks': cidr_blocks_from_rule(sg_rule),
                     'source_security_group_id': source_security_group_id_from_rule(sg_rule),
                     'type': security_group_rule_type(sg_rule)},
                    sg_rules))


def _get_sg_rules_by_sg_id(sg_id: str, rule_type: SecurityGroupCIDRType, sg_rules: List[Dict[str, str]]
                           ) -> List[Dict[str, str]]:
    return list(filter(
        lambda sg_rule:
        sg_rule['security_group_id'] == sg_id and sg_rule['type'] == rule_type.value,
        sg_rules))


def _source_security_group_ids_of_type_from_rule(security_group: Dict, rule_type: SecurityGroupCIDRType,
                                                 sg_rules: List[Dict[str, str]]):
    sg_rules_by_sg_id = _get_sg_rules_by_sg_id(security_group['resource_id'], rule_type, sg_rules)
    return list(filter(lambda sg_id: sg_id is not None,
                       list(set([r['source_security_group_id'] for r in sg_rules_by_sg_id]))))


def _cidr_of_type_from_rule(security_group: Dict, rule_type: SecurityGroupCIDRType,
                            sg_rules: List[Dict[str, str]]):
    sg_rules_by_sg_id = _get_sg_rules_by_sg_id(security_group['resource_id'], rule_type, sg_rules)

    return list(filter(lambda sg_rule: sg_rule.get('cidr_blocks', None) is not None, sg_rules_by_sg_id))


def _get_sgs_of_type(security_group: Dict, sg_type: SecurityGroupCIDRType,
                     sg_rules: List[Dict[str, str]]) -> List[str]:
    return security_groups_ids_from_type_property(security_group, sg_type.value) or \
           _source_security_group_ids_of_type_from_rule(security_group, sg_type, sg_rules)


def __is_valid_cidr_object(sg_rule: Union[str, Dict[str, str]]) -> bool:
    if isinstance(sg_rule, str):
        return False
    return 'cidr_blocks' in sg_rule


def _get_cidr_of_type(security_group: Dict, cidr_type: SecurityGroupCIDRType,
                      sg_rules: List[Dict[str, str]]) -> List[SecurityGroupCIDR]:
    sg_cidr = cidr_from_type_property(security_group, cidr_type.value) or \
              _cidr_of_type_from_rule(security_group, cidr_type, sg_rules)

    sg_cidr = list(filter(lambda cidr: __is_valid_cidr_object(cidr), sg_cidr))

    if not sg_cidr:
        return []

    return list(map(lambda cidr: SecurityGroupCIDRLoader(cidr, cidr_type).load(), sg_cidr))


class SecurityGroupCIDRLoader:

    def __init__(self, security_group_cidr: dict, cidr_type: SecurityGroupCIDRType):
        self.security_group_cidr = security_group_cidr
        self.cidr_type = cidr_type

    def load(self):
        cidr_blocks = self.security_group_cidr.get('cidr_blocks', [])
        description = self.security_group_cidr.get('description', '')
        protocol = self.security_group_cidr.get('protocol', '')
        from_port = self.security_group_cidr.get('from_port', '')
        to_port = self.security_group_cidr.get('to_port', '')

        return SecurityGroupCIDR(
            cidr_blocks=cidr_blocks,
            description=description,
            type=self.cidr_type,
            protocol=protocol,
            from_port=from_port,
            to_port=to_port
        )


class SecurityGroupsLoader:

    def __init__(self, otm: TFPlanOTM, tfplan: {}):
        self.otm = otm

        self._resources = tfplan['resource']
        self._sg_rules: List[Dict[str, str]] = []

    def load(self):
        self._sg_rules = _get_security_group_rules(self._resources)
        for resource in self._resources:
            if resource['resource_type'] in SECURITY_GROUPS_TYPES:
                self.otm.security_groups.append(self.__build_security_group(resource))

    def __build_security_group(self, resource: {}) -> SecurityGroup:
        return SecurityGroup(
            security_group_id=resource['resource_id'],
            name=resource['resource_name'],
            ingress_sgs=_get_sgs_of_type(resource, SecurityGroupCIDRType.INGRESS, self._sg_rules),
            egress_sgs=_get_sgs_of_type(resource, SecurityGroupCIDRType.EGRESS, self._sg_rules),
            ingress_cidr=_get_cidr_of_type(resource, SecurityGroupCIDRType.INGRESS, self._sg_rules),
            egress_cidr=_get_cidr_of_type(resource, SecurityGroupCIDRType.EGRESS, self._sg_rules),
        )
