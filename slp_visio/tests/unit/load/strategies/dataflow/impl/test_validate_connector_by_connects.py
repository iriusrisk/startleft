from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.connector.impl.validate_connector_by_connects import \
    ValidateConnectorByConnects


class TestValidateConnectorByConnects:

    @pytest.mark.parametrize('connector_shape_id_first,connector_shape_id_second', {
        (1001, 1001),
        (1001, 1002),
        (1002, 1001)
    })
    def test_validate_connector_ok(self, connector_shape_id_first, connector_shape_id_second):
        # GIVEN a visio connector shape
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1, connector_shape_id=connector_shape_id_first),
                      MagicMock(from_rel='EndX', shape_id=2, connector_shape_id=connector_shape_id_second)])

        # WHEN the connector is validated
        strategy = ValidateConnectorByConnects()
        result = strategy.is_connector(shape)

        # THEN is a valid connector
        assert result

    @pytest.mark.parametrize('connector_shape_id_first,connector_shape_id_second', {
        (1002, 1003),
        (0, 0),
        (None, None)
    })
    def test_validate_with_connects_wrong_connector_shape_id(self, connector_shape_id_first, connector_shape_id_second):
        # GIVEN a visio connector shape
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1, connector_shape_id=connector_shape_id_first),
                      MagicMock(from_rel='EndX', shape_id=2, connector_shape_id=connector_shape_id_second)])

        # WHEN the connector is validated
        strategy = ValidateConnectorByConnects()
        result = strategy.is_connector(shape)

        # THEN is not a valid connector
        assert not result
