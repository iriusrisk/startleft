from vsdx import Shape

from slp_visio.slp_visio.load.strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategy

LUCID_LINE = 'com.lucidchart.Line'


class ConnectorIdentifierByLucidLineName(ConnectorIdentifierStrategy):
    """
    Strategy to know if a shape is a connector
    The shape name must start with "com.lucidchart.Line"
    """

    def is_connector(self, shape: Shape) -> bool:
        name = shape.shape_name
        if name and name.startswith(f'{LUCID_LINE}'):
            return True
