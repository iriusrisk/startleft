from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.strategies.boundary.boundary_identifier_strategy import BoundaryIdentifierStrategy, \
    BoundaryIdentifierStrategyContainer


@register(BoundaryIdentifierStrategyContainer.visio_strategies)
class BoundaryIdentifierByCurvedPanel(BoundaryIdentifierStrategy):
    """
    Strategy to know if a shape is a boundary
    The shape must have name and must contain 'Curved panel'
    """

    def is_boundary(self, shape: Shape) -> bool:
        return shape.shape_name is not None and 'Curved panel' in shape.shape_name
