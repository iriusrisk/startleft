

from slp_tfplan.slp_tfplan.matcher.component_security_group_match_strategies import \
    ComponentSecurityGroupMatchStrategy, ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy, \
    ComponentMatchStrategySecurityGroupByGraphStrategy
from slp_tfplan.slp_tfplan.strategy.strategy import get_strategies


class TestComponentSecurityGroupMatchStrategyGroup:

    def test_get_strategies(self):
        # WHEN we get the strategies from ComponentSecurityGroupMatchStrategyGroup
        strategies = get_strategies(ComponentSecurityGroupMatchStrategy)

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0].__class__ == ComponentMatchStrategySecurityGroupByGraphStrategy
        assert strategies[1].__class__ == ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy
