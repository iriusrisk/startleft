from unittest.mock import MagicMock

from slp_tfplan.slp_tfplan.matcher import SGAndSGRulesMatcher

sg_1 = MagicMock()
sg_rule_1 = MagicMock()
sg_rule_2 = MagicMock()


def are_sgs_related(resource_1, resource_2, **kwargs):
    # 'sg_1' related to 'sg_rule_1'
    return resource_1 == sg_1 and resource_2 == sg_rule_1


class TestSGAndSGRulesMatcher:

    def test_sg_match(self):
        # GIVEN a security group
        # AND a list of security group rules
        # AND a matcher that returns the relationship between them
        matcher = SGAndSGRulesMatcher(sg_1, [sg_rule_1, sg_rule_2], MagicMock())
        matcher._are_related = are_sgs_related

        # WHEN SGAndSGRulesMatcher::match is called
        related_sg_rule = matcher.match()

        # THEN the related sg rules is only sg_rule_1
        assert len(related_sg_rule) == 1
        assert related_sg_rule[0] == sg_rule_1
