from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_connects import CreateConnectorByConnects


class TestCreateConnectorByConnects:

    def test_create_connector_ok(self):
        # GIVEN a visio connector shape
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)])

        # WHEN the connector is created
        strategy = CreateConnectorByConnects()
        diagram_connector = strategy.create_connector(shape)

        # THEN the returned diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == 1
        assert diagram_connector.to_id == 2

    def test_create_connector_reversed_ok(self):
        # GIVEN a visio connector shape with reversed relationship
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)])

        # WHEN we try to create the connector
        strategy = CreateConnectorByConnects()
        diagram_connector = strategy.create_connector(shape)

        # THEN the returned diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == 2
        assert diagram_connector.to_id == 1

    def test_create_connector_incomplete_connectors(self):
        # GIVEN a visio connector shape with incomplete connectors
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1)])

        # WHEN we try to create the connector
        strategy = CreateConnectorByConnects()
        diagram_connector = strategy.create_connector(shape)

        # THEN no diagram connector is returned
        assert not diagram_connector

    def test_create_connector_self_pointing(self):
        # GIVEN a visio connector shape self pointing
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=1)])

        # WHEN we try to create the connector
        strategy = CreateConnectorByConnects()
        diagram_connector = strategy.create_connector(shape)

        # THEN no diagram connector is returned
        assert not diagram_connector

    @pytest.mark.parametrize('shape,cell_values,master_name,from_shape,to_shape,bidirectional', [
        # Control case
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, None, 1, 2, False, id='control'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, 'Custom Arrow', 1, 2, False, id='control_inverted'),
        # Created left to right, arrow changed left to right
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 1, 2, False, id='left_to_right_arrow_changed_left_to_right'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 1, 2, False, id='left_to_right_arrow_changed_left_to_right_inverted'),
        # Created left to right, arrow changed right to left
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': None}, None, 2, 1, False, id='left_to_right_arrow_changed_right_to_left'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': None}, None, 2, 1, False, id='left_to_right_arrow_changed_right_to_left_inverted'),
        # Created right to left, arrow changed right to left
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 2, 1, False, id='right_to_left_arrow_changed_right_to_left'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 2, 1, False, id='right_to_left_arrow_changed_right_to_left_inverted'),
        # Created right to left, arrow changed left to right
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': None}, None, 1, 2, False, id='right_to_left_arrow_changed_left_to_right'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': None}, None, 1, 2, False, id='right_to_left_arrow_changed_left_to_right_inverted'),
        # Invalid BeginArrow/EndArrow combinations
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '0', 'EndArrow': None}, None, 1, 2, False, id='invalid_begin_0_no_end'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '0'}, None, 1, 2, False, id='invalid_no_begin_end_0'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '0', 'EndArrow': '0'}, None, 1, 2, False, id='invalid_begin_0_end_0'),
        # Created left to right, arrow changed to bidirectional
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': '13'}, None, 1, 2, True, id='left_to_right_arrow_changed_bidirectional'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': '13'}, None, 2, 1, True, id='left_to_right_arrow_changed_bidirectional_inverted'),
        # Created right to left, arrow changed to bidirectional
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': '13'}, None, 2, 1, True, id='right_to_left_arrow_changed_bidirectional'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': '13'}, None, 1, 2, True, id='right_to_left_arrow_changed_bidirectional_inverted'),
        # Created left to right, shape changed to bidirectional
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, 'Simple Double Arrow', 1, 2, True, id='left_to_right_shape_changed_bidirectional'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': None}, 'Line Double Arrow', 2, 1, True, id='left_to_right_shape_changed_bidirectional_inverted'),
        # Created right to left, shape changed to bidirectional
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': None}, 'Arced Line Double Arrow', 2, 1, True, id='right_to_left_shape_changed_bidirectional'),
        pytest.param(MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, 'Block Double Arrow', 1, 2, True, id='right_to_left_shape_changed_bidirectional_inverted')
    ])
    def test_create_connector_modified_manually(self, shape, cell_values, master_name, from_shape, to_shape, bidirectional):
        # GIVEN a mocked visio connector
        shape.cell_value.side_effect = cell_values.get
        shape.master_page.name = master_name

        # WHEN we try to create the connector
        diagram_connector = CreateConnectorByConnects().create_connector(shape)

        # THEN the returned diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == from_shape
        assert diagram_connector.to_id == to_shape
        assert diagram_connector.bidirectional == bidirectional

    def test_connector_without_connects(self):
        # GIVEN a visio connector shape without connects
        shape = MagicMock(ID=1001)

        # WHEN we try to create the connector
        strategy = CreateConnectorByConnects()
        diagram_connector = strategy.create_connector(shape)

        # THEN no diagram connector is created
        assert not diagram_connector
