from unittest.mock import MagicMock

from startleft.startleft.diagram.objects.visio.visio_diagram_factories import VisioConnectorFactory


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

