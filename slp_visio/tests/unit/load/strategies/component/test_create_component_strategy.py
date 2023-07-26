from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategyContainer
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_shape_text import CreateComponentByShapeText
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_master_page_name import \
    CreateComponentByMasterPageName

class TestCreateComponentStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateComponentStrategy
        strategies = [x.cls for x in CreateComponentStrategyContainer.visio_strategies.args]

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0] == CreateComponentByShapeText
        assert strategies[1] == CreateComponentByMasterPageName
