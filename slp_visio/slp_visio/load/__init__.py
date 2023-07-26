from .strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategyContainer
from .strategies.connector.create_connector_strategy import CreateConnectorStrategyContainer
from .strategies.connector.impl import connector_identifier_by_connects, create_connector_by_connects, \
    create_connector_by_line_coordinates
from .strategies.component.impl import component_identifier_by_shape_text, create_component_by_shape_text, \
    component_identifier_by_master_page_name, create_component_by_master_page_name
from .strategies.boundary.impl import boundary_identifier_by_curved_panel

from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategyContainer

ComponentIdentifierStrategyContainer().wire(packages=[__name__])
ConnectorIdentifierStrategyContainer().wire(packages=[__name__])
CreateConnectorStrategyContainer().wire(packages=[__name__])