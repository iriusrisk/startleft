import logging
from typing import Optional, List

from dependency_injector.wiring import inject, Provide

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, DiagramConnector
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategyContainer
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy, \
    CreateConnectorStrategyContainer

logger = logging.getLogger(__name__)


class VisioComponentFactory:

    @inject
    def __init__(self, strategies: List[CreateComponentStrategy] = Provide[
        CreateComponentStrategyContainer.visio_strategies]):
        self.strategies = strategies

    def create_component(self, shape, origin, representer) -> DiagramComponent:
        logger.debug(f'creating diagramComponent from shape {shape.ID}')
        for strategy in self.strategies:
            logger.debug(f'Applying  {strategy.__class__.__name__}')
            component = strategy.create_component(shape, origin=origin, representer=representer)
            if component:
                logger.debug(f'Created diagramComponent from shape {shape.ID}')
                return component
        logger.debug(f'No diagramComponent was created from shape {shape.ID}')


class VisioConnectorFactory:

    @inject
    def __init__(self, strategies: List[CreateConnectorStrategy] = Provide[
        CreateConnectorStrategyContainer.visio_strategies]):
        self.strategies = strategies

    def create_connector(self, shape) -> Optional[DiagramConnector]:
        for strategy in self.strategies:
            connector = strategy.create_connector(shape)
            if connector:
                return connector
