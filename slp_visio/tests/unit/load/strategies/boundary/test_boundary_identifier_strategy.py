from slp_visio.slp_visio.load.strategies.boundary.impl.boundary_identifier_by_curved_panel import BoundaryIdentifierByCurvedPanel
from slp_visio.slp_visio.load.strategies.boundary.boundary_identifier_strategy import BoundaryIdentifierStrategy


class TestBoundaryIdentifierStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateBoundaryStrategy
        strategies = BoundaryIdentifierStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 1

        # AND we have the expected implementations
        assert strategies[0].__class__ == BoundaryIdentifierByCurvedPanel