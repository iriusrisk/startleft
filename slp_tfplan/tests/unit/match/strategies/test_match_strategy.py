from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategy, MatchStrategyContainer
from slp_tfplan.tests.util.builders import get_instance_classes


class TestMatchStrategy:

    def test_get_strategies(self):
        # GIVEN all the subclasses of the MatchStrategy interface
        match_strategy_subclasses = MatchStrategy.__subclasses__()

        # AND the MatchStrategyContainer
        match_strategy_container = MatchStrategyContainer()

        # AND all the instances for component_sg_match_strategies in MatchStrategyContainer
        component_sg_match_strategy_instances = match_strategy_container.component_sg_match_strategies

        # AND all the instances for sg_match_strategies in MatchStrategyContainer
        sg_match_strategy_instances = match_strategy_container.sg_match_strategies

        # WHEN we merge all instances and extract their classes
        all_instance_classes = get_instance_classes(component_sg_match_strategy_instances) + \
                               get_instance_classes(sg_match_strategy_instances)

        # THEN the subclasses and the instances match
        assert match_strategy_subclasses == all_instance_classes
