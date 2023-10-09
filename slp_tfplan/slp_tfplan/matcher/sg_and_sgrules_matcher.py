from typing import Dict, List

from dependency_injector.wiring import inject, Provide

from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourceMatcher, ResourcesMatcherContainer


class SGAndSGRulesMatcher:
    """
    This class is responsible for matching security groups and security groups rules.
    """
    @inject
    def __init__(self,
                 security_group: Dict, security_group_rules: List[Dict],
                 relationships_extractor: RelationshipsExtractor,
                 sg_rule_matcher: ResourceMatcher = Provide[ResourcesMatcherContainer.sg_rule_matcher]):
        # Data structures
        self._security_group: Dict = security_group
        self._security_group_rules: List[Dict] = security_group_rules
        self._relationships_extractor: RelationshipsExtractor = relationships_extractor

        # Injected dependencies
        self._are_related = sg_rule_matcher.are_related

    def match(self) -> List[Dict]:
        """
        Returns a list of security group rules related with the security group.
        :return: List of security group rules
        """
        related_sg_rule = []
        for sg_rule in self._security_group_rules:
            if self._are_related(self._security_group, sg_rule, relationships_extractor=self._relationships_extractor):
                related_sg_rule.append(sg_rule)

        return related_sg_rule
