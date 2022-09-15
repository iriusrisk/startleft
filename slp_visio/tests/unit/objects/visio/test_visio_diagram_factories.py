from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.objects.visio_diagram_factories import VisioConnectorFactory


class TestVisioConnectorFactory:

    def test_create_connector_ok(self):
        # GIVEN visio connector shape
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)])

        # WHEN a connector is created
        visio_connector = VisioConnectorFactory()
        diagram_connector = visio_connector.create_connector(shape)

        # THEN a diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == 1
        assert diagram_connector.to_id == 2

    def test_create_connector_reversed_ok(self):
        # GIVEN visio connector shape with reversed relationship
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)])

        # WHEN a connector is created
        visio_connector = VisioConnectorFactory()
        diagram_connector = visio_connector.create_connector(shape)

        # THEN a diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == 2
        assert diagram_connector.to_id == 1

    def test_create_connector_incomplete_connectors(self):
        # GIVEN visio connector shape with incomplete connectors
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1)])

        # WHEN a connector is created
        visio_connector = VisioConnectorFactory()
        diagram_connector = visio_connector.create_connector(shape)

        # THEN None diagram connector is returned
        assert not diagram_connector

    def test_create_connector_self_pointing(self):
        # GIVEN visio connector shape self pointing
        shape = MagicMock(
            ID=1001,
            connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=1)])

        # WHEN a connector is created
        visio_connector = VisioConnectorFactory()
        diagram_connector = visio_connector.create_connector(shape)

        # THEN None diagram connector is returned
        assert not diagram_connector

    @pytest.mark.parametrize('shape,cell_values,master_name,from_shape,to_shape', [
        # Control case
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, None, 1, 2),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': None}, 'Custom Arrow', 1, 2),
        # Created left to right, arrow changed left to right
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 1, 2),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 1, 2),
        # Created left to right, arrow changed right to left
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': None}, None, 2, 1),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=2), MagicMock(from_rel='BeginX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': None}, None, 2, 1),
        # Created right to left, arrow changed right to left
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 2, 1),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '13'}, None, 2, 1),
        # Created right to left, arrow changed left to right
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=2), MagicMock(from_rel='EndX', shape_id=1)]), {'BeginArrow': '13', 'EndArrow': None}, None, 1, 2),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='EndX', shape_id=1), MagicMock(from_rel='BeginX', shape_id=2)]), {'BeginArrow': '13', 'EndArrow': None}, None, 1, 2),
        # Invalid BeginArrow/EndArrow combinations
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '0', 'EndArrow': None}, None, 1, 2),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': None, 'EndArrow': '0'}, None, 1, 2),
        (MagicMock(ID=1001, connects=[MagicMock(from_rel='BeginX', shape_id=1), MagicMock(from_rel='EndX', shape_id=2)]), {'BeginArrow': '0', 'EndArrow': '0'}, None, 1, 2)
    ])
    def test_create_connector_modified_manually(self, shape, cell_values, master_name, from_shape, to_shape):
        # GIVEN a mocked visio connector
        shape.cell_value.side_effect = cell_values.get
        shape.master_page.name = master_name

        # WHEN a connector is created
        diagram_connector = VisioConnectorFactory().create_connector(shape)

        # THEN a diagram connector has the following properties
        assert diagram_connector.id == 1001
        assert diagram_connector.from_id == from_shape
        assert diagram_connector.to_id == to_shape

