from sl_util.sl_util.injection import register
from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup


@register(MatchStrategyContainer.sg_sg_match_strategies)
class SecurityGroupByConfigurationStrategy(MatchStrategy):
    """
    Two Security Groups SG1 and SG2 are related if the ID of SG1 is in the ingress_ids of the SG2 or if the
    ID of the SG2 is in the egress_ids of the SG1.
    """

    def are_related(self, source_security_group: SecurityGroup, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return source_security_group.id in target_security_group.ingress_sgs \
               or target_security_group.id in source_security_group.egress_sgs


@register(MatchStrategyContainer.sg_sg_match_strategies)
class SecurityGroupByGraphStrategy(MatchStrategy):
    """
    Two Security Groups are related if there is a straight relationship between them in the tfgraph. This means that
    there is a relationships between a SG1 and a SG2 with no mapped components in the middle.
    """

    def are_related(self, source_security_group: SecurityGroup, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return kwargs['relationships_extractor'].exist_valid_path(target_security_group.id, source_security_group.id)
