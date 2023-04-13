from vsdx import Shape

from slp_visio.slp_visio.load.strategies.connector.validate_connector_strategy import ValidateConnectorStrategy


class ValidateConnectorByConnects(ValidateConnectorStrategy):
    """
    Strategy to know if a shape is a connector
    The shape must have connects and each connector_shape_id must match with the shape id
    """

    def is_connector(self, shape: Shape) -> bool:
        for connect in shape.connects:
            if shape.ID == connect.connector_shape_id:
                return True
        return False