import abc

from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup, TFPlanComponent


class SecurityGroupMatchStrategy:
    # TODO Create documentation per strategy group

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'are_related') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def are_related(self, source_security_group: TFPlanComponent, target_security_group: SecurityGroup, **kwargs) -> bool:
        raise NotImplementedError


class SecurityGroupByConfigurationStrategy(SecurityGroupMatchStrategy):
    def are_related(self, source_security_group: TFPlanComponent, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return source_security_group.id in target_security_group.ingress_sgs \
            or target_security_group.id in source_security_group.egress_sgs


class SecurityGroupByGraphStrategy(SecurityGroupMatchStrategy):
    def are_related(self, source_security_group: TFPlanComponent, target_security_group: SecurityGroup,
                    **kwargs) -> bool:
        return kwargs['relationships_extractor'].exist_valid_path(target_security_group.id, source_security_group.id)


