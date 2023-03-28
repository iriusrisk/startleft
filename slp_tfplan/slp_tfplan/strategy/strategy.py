def get_strategies(cls):
    return [obj() for obj in _get_subclasses(cls)]


def _get_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield subclass
