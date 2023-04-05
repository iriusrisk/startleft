from typing import List, Dict, Literal

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanSecurityGroup, TfplanOTM
from slp_tfplan.slp_tfplan.load.resource_data_extractors import security_groups_ids_from_ingress_property, \
    security_groups_ids_from_egress_property, security_group_id_from_rule, \
    source_security_group_id_from_rule, security_group_rule_type

SECURITY_GROUPS_TYPES = ['aws_security_group']
SECURITY_GROUP_RULE_TYPES = ['aws_security_group_rule']


def _get_security_group_rules(resources: List[Dict]) -> List[Dict[str, str]]:
    sg_rules = list(filter(lambda r: r['resource_type'] in SECURITY_GROUP_RULE_TYPES, resources))
    if not sg_rules:
        return []

    return list(map(lambda sg_rule:
                    {'security_group_id': security_group_id_from_rule(sg_rule),
                     'source_security_group_id': source_security_group_id_from_rule(sg_rule),
                     'type': security_group_rule_type(sg_rule)},
                    sg_rules))


def _security_group_ids_from_rule(security_group: Dict, sg_rules: List[Dict[str, str]],
                                  rule_type: Literal['ingress', 'egress']):
    rules = list(filter(
        lambda sg_rule:
        sg_rule['security_group_id'] == security_group['resource_id'] and sg_rule['type'] == rule_type,
        sg_rules))

    return list(set([r['source_security_group_id'] for r in rules]))


def security_groups_ids_from_ingress_rule(security_group: Dict, sg_rules: List[Dict[str, str]]) -> List[str]:
    return _security_group_ids_from_rule(security_group, sg_rules, 'ingress')


def security_groups_ids_from_egress_rule(security_group: Dict, sg_rules: List[Dict[str, str]]) -> List[str]:
    return _security_group_ids_from_rule(security_group, sg_rules, 'egress')


class SecurityGroupsLoader:

    def __init__(self, otm: TfplanOTM, tfplan: {}):
        self.otm = otm
        self.resources = tfplan['resource']

        self.sg_rules: List[Dict[str, str]] = []

    def load(self):
        self.sg_rules = _get_security_group_rules(self.resources)

        for resource in self.resources:
            if resource['resource_type'] in SECURITY_GROUPS_TYPES:
                self.otm.security_groups.append(self.__build_security_group(resource))

    def __build_security_group(self, resource: {}) -> TFPlanSecurityGroup:
        return TFPlanSecurityGroup(
            security_group_id=resource['resource_id'],
            ingress_sgs=security_groups_ids_from_ingress_property(resource) or security_groups_ids_from_ingress_rule(resource, self.sg_rules),
            egress_sgs=security_groups_ids_from_egress_property(resource) or security_groups_ids_from_egress_rule(resource, self.sg_rules),
        )
