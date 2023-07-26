from vsdx import Shape

from slp_visio.slp_visio.load.strategies.boundary.boundary_identifier_strategy import BoundaryIdentifierStrategy


class BoundaryIdentifier:
    """
    Identifies if a Visio Shape is a component of DiagramComponentOrigin.BOUNDARY type
    when we parse from Visio Shape to a DiagramComponent class
    """

    @staticmethod
    def is_boundary(shape: Shape) -> bool:
        for strategy in BoundaryIdentifierStrategy.get_strategies():
            if strategy.is_boundary(shape):
                return True

        return False
