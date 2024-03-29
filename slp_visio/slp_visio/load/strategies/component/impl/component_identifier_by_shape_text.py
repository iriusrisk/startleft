from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.connector_identifier import ConnectorIdentifier
from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy, \
    ComponentIdentifierStrategyContainer
from slp_visio.slp_visio.util.visio import get_shape_text


@register(ComponentIdentifierStrategyContainer.visio_strategies)
class ComponentIdentifierByShapeText(ComponentIdentifierStrategy):
    """
    Strategy to know if a shape is a component
    The shape must have the text property and must not be a connector
    """

    def __init__(self):
        self.connector_identifier = ConnectorIdentifier()

    def is_component(self, shape: Shape) -> bool:
        text = get_shape_text(shape)
        is_connector = self.connector_identifier.is_connector(shape)
        return text and not is_connector
