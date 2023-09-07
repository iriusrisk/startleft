from functools import lru_cache
from typing import List

from dependency_injector.wiring import inject, Provide
from vsdx import Shape

from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy, \
    ComponentIdentifierStrategyContainer


class ComponentIdentifier:
    """
    Identifies if a Visio Shape is a representation of a component
    when we parse from Visio Shape to a DiagramComponent class
    """

    @inject
    def __init__(self, strategies: List[ComponentIdentifierStrategy] = Provide[
        ComponentIdentifierStrategyContainer.visio_strategies]):
        self.strategies = strategies

    @lru_cache(maxsize=None)
    def is_component(self, shape: Shape) -> bool:
        for strategy in self.strategies:
            if strategy.is_component(shape):
                return True

        return False
