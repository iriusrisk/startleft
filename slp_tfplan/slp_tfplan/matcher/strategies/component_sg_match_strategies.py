from sl_util.sl_util.injection import register
from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup, TFPlanComponent


@register(MatchStrategyContainer.component_sg_match_strategies)
class ComponentMatchStrategySecurityGroupByGraphStrategy(MatchStrategy):
    """
    A component belongs to a security group if there is a tfgraph relationship between the SG and the component
    in any direction.
    """

    def are_related(self, component: TFPlanComponent, security_group: SecurityGroup, **kwargs) -> bool:
        relationships_extractor = kwargs['relationships_extractor']

        return relationships_extractor.exist_valid_path(component.tf_resource_id, security_group.id) or \
            relationships_extractor.exist_valid_path(security_group.id, component.tf_resource_id)


@register(MatchStrategyContainer.component_sg_match_strategies)
class ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy(MatchStrategy):
    """
    A component belongs to a security group if there is a relationship from the component to a Launch Template in the
    tfgraph and the ID of the security group is referenced in that Launch Template.
    """
    def are_related(self, component: TFPlanComponent, security_group: SecurityGroup, **kwargs) -> bool:
        relationships_extractor = kwargs['relationships_extractor']
        launch_templates = kwargs['launch_templates']

        for launch_template in launch_templates:
            if relationships_extractor.exist_valid_path(component.tf_resource_id, launch_template.id) and \
                    security_group.id in launch_template.security_groups_ids:
                return True

        return False
