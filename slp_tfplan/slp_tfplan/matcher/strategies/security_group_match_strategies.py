from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup, TFPlanComponent
from slp_tfplan.slp_tfplan.util.injection import register


@register(MatchStrategyContainer.sg_match_strategies)
class SecurityGroupByConfigurationStrategy(MatchStrategy):
    def are_related(self, source_security_group: TFPlanComponent, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return source_security_group.id in target_security_group.ingress_sgs \
            or target_security_group.id in source_security_group.egress_sgs


@register(MatchStrategyContainer.sg_match_strategies)
class SecurityGroupByGraphStrategy(MatchStrategy):
    def are_related(self, source_security_group: TFPlanComponent, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return kwargs['relationships_extractor'].exist_valid_path(target_security_group.id, source_security_group.id)
