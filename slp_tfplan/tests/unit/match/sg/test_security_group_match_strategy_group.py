from slp_tfplan.slp_tfplan.matcher.security_group_match_strategies import SecurityGroupMatchStrategy, \
    SecurityGroupByConfigurationStrategy, SecurityGroupByGraphStrategy
from slp_tfplan.slp_tfplan.strategy.strategy import get_strategies


class TestSecurityGroupMatchStrategyGroup:

    def test_get_strategies(self):
        # WHEN we get the strategies from SecurityGroupMatchStrategyGroup
        strategies = get_strategies(SecurityGroupMatchStrategy)

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0].__class__ == SecurityGroupByConfigurationStrategy
        assert strategies[1].__class__ == SecurityGroupByGraphStrategy
