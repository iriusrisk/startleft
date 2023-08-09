from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.connector_identifier import ConnectorIdentifier
from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy, \
    ComponentIdentifierStrategyContainer


@register(ComponentIdentifierStrategyContainer.visio_strategies)
class ComponentIdentifierByMasterPageName(ComponentIdentifierStrategy):
    """
    Strategy to know if a shape is a component
    The shape must have a master with name and must not be a connector
    """

    def __init__(self):
        self.connector_identifier = ConnectorIdentifier()

    def is_component(self, shape: Shape) -> bool:
        name = self.get_master_page_name(shape)
        is_connector = self.connector_identifier.is_connector(shape)
        return name and not is_connector

    @staticmethod
    def get_master_page_name(shape: Shape) -> str:
        if not shape.master_page:
            return ""

        result = shape.master_page.name

        return (result or "").strip()
