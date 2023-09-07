from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import \
    ComponentIdentifierStrategyContainer
from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_master_page_name import \
    ComponentIdentifierByMasterPageName
from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_shape_text import \
    ComponentIdentifierByShapeText


class TestComponentIdentifierStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from ComponentIdentifierStrategy
        strategies = [x.cls for x in ComponentIdentifierStrategyContainer.visio_strategies.args]

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0] == ComponentIdentifierByShapeText
        assert strategies[1] == ComponentIdentifierByMasterPageName