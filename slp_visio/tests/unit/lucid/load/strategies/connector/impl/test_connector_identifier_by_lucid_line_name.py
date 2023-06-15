from _elementtree import Element

import pytest
from vsdx import Shape

from slp_visio.slp_visio.lucid.load.strategies.connector.impl.connector_identifier_by_lucid_line_name import \
    ConnectorIdentifierByLucidLineName


class TestConnectorIdentifierByLucidLineName:

    @pytest.mark.parametrize('name', {
        'com.lucidchart.Line',
        'com.lucidchart.Line.30',
        'com.lucidchart.Line.abc.def',
    })
    def test_validate_connector_ok(self, name):
        # GIVEN a visio connector shape
        element = Element('Shape', {'NameU': name})
        shape = Shape(element, None, None)

        # WHEN the connector is validated
        strategy = ConnectorIdentifierByLucidLineName()
        result = strategy.is_connector(shape)

        # THEN is a valid connector
        assert result

    @pytest.mark.parametrize('name', {
        'lucidchart.Line',
        'Line.30',
        'com_lucidchart_Line.abc.def',
        '',
        None
    })
    def test_validate_connector_wrong_name(self, name):
        # GIVEN a visio connector shape
        element = Element('Shape', {'NameU': name})
        shape = Shape(element, None, None)

        # WHEN the connector is validated
        strategy = ConnectorIdentifierByLucidLineName()
        result = strategy.is_connector(shape)

        # THEN is a valid connector
        assert not result
