from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_shape_text import CreateComponentByShapeText


class TestCreateComponentStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateComponentStrategy
        strategies = CreateComponentStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 1

        # AND we have the expected implementations
        assert strategies[0].__class__ == CreateComponentByShapeText
