from functools import lru_cache
from typing import List

from dependency_injector.wiring import inject, Provide
from vsdx import Shape

from slp_visio.slp_visio.load.strategies.boundary.boundary_identifier_strategy import BoundaryIdentifierStrategy, \
    BoundaryIdentifierStrategyContainer


class BoundaryIdentifier:
    """
    Identifies if a Visio Shape is a component of DiagramComponentOrigin.BOUNDARY type
    when we parse from Visio Shape to a DiagramComponent class
    """

    @inject
    def __init__(self, strategies: List[BoundaryIdentifierStrategy] = Provide[
        BoundaryIdentifierStrategyContainer.visio_strategies]):
        self.strategies = strategies

    @lru_cache(maxsize=None)
    def is_boundary(self, shape: Shape) -> bool:
        for strategy in self.strategies:
            if strategy.is_boundary(shape):
                return True

        return False
