from unittest.mock import Mock

from slp_tfplan.slp_tfplan.matcher.strategies.sg_sg_rule_match_strategies import \
    MatchSecurityGroupRuleBySecurityGroupIdStrategy, MatchSecurityGroupRuleByGraphStrategy

_sg_1 = {'resource_id': 'SG1'}
_sg_rule1 = {'resource_id': 'SG_R1', 'security_group_id': 'SG1'}
_sg_rule2 = {'resource_id': 'SG_R2', 'security_group_id': 'SG2'}


class TestMatchSecurityGroupRuleBySecurityGroupIdStrategy:

    def test_is_related(self):
        # GIVEN a sg rule with the security_group_id is equals to sg resource id
        # WHEN MatchSecurityGroupRuleBySecurityGroupIdStrategy::are_related is called
        result = MatchSecurityGroupRuleBySecurityGroupIdStrategy().are_related(_sg_1, _sg_rule1)

        # THEN the strategy returns True
        assert result is True

    def test_not_related(self):
        # GIVEN a sg rule with the security_group_id is distinct to sg resource id
        # WHEN MatchSecurityGroupRuleBySecurityGroupIdStrategy::are_related is called
        result = MatchSecurityGroupRuleBySecurityGroupIdStrategy().are_related(_sg_1, _sg_rule2)

        # THEN the strategy returns False
        assert result is False


class TestMatchSecurityGroupRuleByGraphStrategy:

    def test_no_graph_relationship_no_match(self):
        # GIVEN any two mocked SGs
        mocked_sgs = [Mock(), Mock()]

        # AND a relationships_extractor which returns no relationships between them
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda sg_a, sg_b: False

        # WHEN MatchSecurityGroupRuleByGraphStrategy::are_related is called
        result = MatchSecurityGroupRuleByGraphStrategy() \
            .are_related(*mocked_sgs, relationships_extractor=relationships_extractor)

        # THEN the strategy returns False
        assert result is False

    def test_match_when_graph_relationship(self):
        # GIVEN a mocked relationship from _sg_1 to _sg_rule1
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda sg_r, sg: \
            (sg_r, sg) == (_sg_rule1['resource_id'], _sg_1['resource_id'])

        # WHEN SecurityGroupByGraphStrategy::are_related is called
        result = MatchSecurityGroupRuleByGraphStrategy().are_related(
            _sg_1, _sg_rule1, relationships_extractor=relationships_extractor)

        # THEN the strategy returns True
        assert result is True
