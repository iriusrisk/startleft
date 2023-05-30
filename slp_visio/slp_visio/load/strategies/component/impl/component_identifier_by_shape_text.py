from vsdx import Shape

from slp_visio.slp_visio.load.connector_identifier import ConnectorIdentifier
from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy
from slp_visio.slp_visio.util.visio import get_shape_text


class ComponentIdentifierByShapeText(ComponentIdentifierStrategy):
    """
    Strategy to know if a shape is a component
    The shape must have the text property and must not be a connector
    """

    def is_component(self, shape: Shape) -> bool:
        text = get_shape_text(shape)
        is_connector = ConnectorIdentifier.is_connector(shape)
        return text and not is_connector
