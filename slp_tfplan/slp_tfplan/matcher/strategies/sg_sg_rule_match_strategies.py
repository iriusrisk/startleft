from typing import Dict

from sl_util.sl_util.injection import register
from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer


@register(MatchStrategyContainer.sg_sg_rule_match_strategies)
class MatchSecurityGroupRuleBySecurityGroupIdStrategy(MatchStrategy):
    """
    A security group rule is related with a security group by sg_rule['security_group_id'] being equals
    to security_group['resource_id'].
    """
    def are_related(self, security_group: Dict, security_group_rule: Dict, **kwargs) -> bool:
        return security_group.get('resource_id') == security_group_rule.get('security_group_id')


@register(MatchStrategyContainer.sg_sg_rule_match_strategies)
class MatchSecurityGroupRuleByGraphStrategy(MatchStrategy):
    """
    A security group rule is related with a security group if there is a tfgraph relationship
    between the security group rule and the security group.
    """

    def are_related(self, security_group: Dict, security_group_rule: Dict, **kwargs) -> bool:
        sg_resource_id = security_group.get('resource_id')
        sg_rule_resource_id = security_group_rule.get('resource_id')
        relationships_extractor = kwargs['relationships_extractor']

        return relationships_extractor.exist_valid_path(sg_rule_resource_id, sg_resource_id)
