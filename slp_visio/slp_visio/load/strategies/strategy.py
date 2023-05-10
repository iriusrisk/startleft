import abc


class Strategy(metaclass=abc.ABCMeta):
    """
    Formal Interface to build a strategy
    """

    @classmethod
    def get_strategies(cls):
        return [obj() for obj in cls.__get_subclasses()]

    @classmethod
    def __get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass