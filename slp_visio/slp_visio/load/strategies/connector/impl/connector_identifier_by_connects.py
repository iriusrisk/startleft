from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategy, \
    ConnectorIdentifierStrategyContainer


@register(ConnectorIdentifierStrategyContainer.visio_strategies)
class ConnectorIdentifierByConnects(ConnectorIdentifierStrategy):
    """
    Strategy to know if a shape is a connector
    The shape must have connects and each connector_shape_id must match with the shape id
    """

    def is_connector(self, shape: Shape) -> bool:
        for connect in shape.connects:
            if shape.ID == connect.connector_shape_id:
                return True
        return False
