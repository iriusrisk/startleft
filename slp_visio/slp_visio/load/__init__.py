from .strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategyContainer
from .strategies.connector.create_connector_strategy import CreateConnectorStrategyContainer
from .strategies.connector.impl import connector_identifier_by_connects, create_connector_by_connects, \
    create_connector_by_line_coordinates

from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategyContainer

ComponentIdentifierStrategyContainer().wire(packages=[__name__])
ConnectorIdentifierStrategyContainer().wire(packages=[__name__])
CreateConnectorStrategyContainer().wire(packages=[__name__])