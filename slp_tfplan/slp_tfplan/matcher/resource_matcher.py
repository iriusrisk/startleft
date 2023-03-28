from slp_tfplan.slp_tfplan.strategy.strategy import get_strategies


class ResourcesMatcher:

    def __init__(self, strategy_group):
        self.strategies = get_strategies(strategy_group)

    def are_related(self, object_1, object_2, **kwargs) -> bool:
        for strategy in self.strategies:
            if strategy.are_related(object_1, object_2, **kwargs):
                return True

        return False
