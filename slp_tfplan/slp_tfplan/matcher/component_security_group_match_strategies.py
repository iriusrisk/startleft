import abc

from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup, TFPlanComponent


class ComponentSecurityGroupMatchStrategy:

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'are_related') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def are_related(self, component: TFPlanComponent, security_group: SecurityGroup, **kwargs) -> bool:
        raise NotImplementedError


class ComponentMatchStrategySecurityGroupByGraphStrategy(ComponentSecurityGroupMatchStrategy):
    """
    A component belongs to a security group if there is a relationship between the SG and the component in any direction
    """

    def are_related(self, component: TFPlanComponent, security_group: SecurityGroup, **kwargs) -> bool:
        relationships_extractor = kwargs['relationships_extractor']

        return relationships_extractor.exist_valid_path(component.tf_resource_id, security_group.id) or \
            relationships_extractor.exist_valid_path(security_group.id, component.tf_resource_id)


class ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy(ComponentSecurityGroupMatchStrategy):
    def are_related(self, component: TFPlanComponent, security_group: SecurityGroup, **kwargs) -> bool:
        relationships_extractor = kwargs['relationships_extractor']
        launch_templates = kwargs['launch_templates']

        for launch_template in launch_templates:
            if relationships_extractor.exist_valid_path(component.tf_resource_id, launch_template.id) and \
                    security_group.id in launch_template.security_groups_ids:
                return True

        return False
