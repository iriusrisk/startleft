from .strategies.boundary.boundary_identifier_strategy import BoundaryIdentifierStrategyContainer
from .strategies.component.component_identifier_strategy import ComponentIdentifierStrategyContainer
from .strategies.component.create_component_strategy import CreateComponentStrategyContainer
from .strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategyContainer
from .strategies.connector.create_connector_strategy import CreateConnectorStrategyContainer

BoundaryIdentifierStrategyContainer().wire(packages=[__name__])
ComponentIdentifierStrategyContainer().wire(packages=[__name__])
ConnectorIdentifierStrategyContainer().wire(packages=[__name__])
CreateConnectorStrategyContainer().wire(packages=[__name__])
CreateComponentStrategyContainer().wire(packages=[__name__])
