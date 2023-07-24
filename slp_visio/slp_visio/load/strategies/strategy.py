import abc

def strategy_order(strategy) -> int:
    return strategy.order if hasattr(strategy, 'order') else 0


class Strategy(metaclass=abc.ABCMeta):
    """
    Formal Interface to build a strategy
    """

    @classmethod
    def get_strategies(cls):
        strategies = [obj() for obj in cls.__get_subclasses()]
        strategies.sort(key=strategy_order)
        return strategies

    @classmethod
    def __get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass
