from dependency_injector import providers
from dependency_injector.providers import Singleton


def register(provider_list: providers.List):
    def f(cls):
        provider_list.add_args(Singleton(cls))
        return cls

    return f
