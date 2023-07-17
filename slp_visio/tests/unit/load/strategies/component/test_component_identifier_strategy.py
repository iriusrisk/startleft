from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_master_page_name import \
    ComponentIdentifierByMasterPageName
from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_shape_text import \
    ComponentIdentifierByShapeText
from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy


class TestComponentIdentifierStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateComponentStrategy
        strategies = ComponentIdentifierStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0].__class__ == ComponentIdentifierByShapeText
        assert strategies[1].__class__ == ComponentIdentifierByMasterPageName