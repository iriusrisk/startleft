from unittest.mock import MagicMock, Mock

from pytest import mark, param

from slp_visio.slp_visio.load.strategies.connector.impl.create_connector_by_line_coordinates import \
    CreateConnectorByLineCoordinates


def mock_component(_id, pos):
    x, y = pos[0], pos[1]
    width, height = pos[2], pos[3]
    return MagicMock(ID=_id, begin_x=x, begin_y=y,
                     cells={'Width': Mock(value=width), 'Height': Mock(value=height)},
                     center_x_y=(float(x) + float(width) / 2, float(y) + float(height) / 2))


class TestCreateConnectorByLineCoordinates:
    @mark.parametrize('line,start,end', [
        param(['1040', '-560', '1290', '-560'], ['960', '-600', '80', '80'], ['1290', '-590', '60', '60'],
                     id="perfect_match,strings,big_scale"),
        param([1040, -560, 1290, -560], [960, -600, 80, 80], [1290, -590, 60, 60],
                     id="perfect_match,big_scale"),
        param(['1.04', '-0.56', '1.29', '-0.56'], ['0.96', '-0.6', '0.08', '0.08'], ['1.29', '-0.59', '0.06', '0.06'],
                     id="perfect_match,strings"),
        param([1.04, -0.56, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="perfect_match"),
        param([1.04 + 0.09, -0.56, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected by right tolerance, end connected"),
        param([0.96 - 0.09, -0.56, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected by left tolerance, end connected"),
        param([1.04, -0.6 - 0.09, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected by top tolerance, end connected"),
        param([1.04, -0.6 + 0.08 + 0.09, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected by bottom tolerance, end connected"),
        param([1.04, -0.56, 1.29 - 0.09, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end connected by left tolerance"),
        param([1.04, -0.56, 1.29 + 0.06 + 0.09, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end connected by right tolerance"),
        param([1.04, -0.56, 1.29, -0.59 - 0.09], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end connected by top tolerance"),
        param([1.04, -0.56, 1.29, -0.59 + 0.06 + 0.09], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end connected by bottom tolerance"),
    ])
    def test_create_connector_with_line_touching_component(self, line, start, end):
        # GIVEN a visio connector shape
        shape = Mock(ID=1111, begin_x=line[0], begin_y=line[1], end_x=line[2], end_y=line[3])
        # AND the start component
        start_component = mock_component(222, start)
        # AND the end component
        end_component = mock_component(333, end)

        # WHEN the connector is created
        strategy = CreateConnectorByLineCoordinates()
        diagram_connector = strategy.create_connector(shape, components=[start_component, end_component])

        # THEN the returned diagram connector has the following properties
        assert diagram_connector.id == 1111
        assert diagram_connector.from_id == 222
        assert diagram_connector.to_id == 333
        assert not diagram_connector.bidirectional


    @mark.parametrize('line,start,end', [
        param([1.04 + 0.09 + 0.006, -0.56, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start not connected by right intolerance, end connected"),
        param([0.96 - 0.09 - 0.006, -0.56, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start not connected by left intolerance, end connected"),
        param([1.04, -0.6 + 0.08 + 0.09 + 0.006, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start not connected by bottom intolerance, end connected"),
        param([1.04, -0.6 - 0.09 - 0.006, 1.29, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start not connected by top intolerance, end connected", ),
        param([1.04, -0.56, 1.29 - 0.09 - 0.006, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end not connected by left intolerance"),
        param([1.04, -0.56, 1.29 + 0.06 + 0.09 + 0.006, -0.56], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end not connected by right intolerance"),
        param([1.04, -0.56, 1.29, -0.59 - 0.09 - 0.006], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end not connected by top intolerance"),
        param([1.04, -0.56, 1.29, -0.59 + 0.06 + 0.09 + 0.006], [0.96, -0.6, 0.08, 0.08], [1.29, -0.59, 0.06, 0.06],
                     id="start connected, end not connected by bottom intolerance"),
    ])
    def test_create_connector_with_line_not_touching(self, line, start, end):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001, begin_x=line[0], begin_y=line[1], end_x=line[2], end_y=line[3])
        # AND the start component
        start_component = mock_component(444, start)
        # AND the end component
        end_component = mock_component(555, end)

        # WHEN the connector is created
        strategy = CreateConnectorByLineCoordinates()
        diagram_connector = strategy.create_connector(shape, components=[start_component, end_component])

        # THEN no diagram is returned
        assert not diagram_connector

    def test_create_connector_without_components(self):
        # GIVEN a visio connector shape
        shape = Mock(ID=1001, begin_x=0, begin_y=0, end_x=0, end_y=0)

        # WHEN the connector is created
        strategy = CreateConnectorByLineCoordinates()
        diagram_connector = strategy.create_connector(shape)

        # THEN no diagram is returned
        assert not diagram_connector

    def test_create_connector_invalid_line(self):
        # GIVEN a visio connector shape
        shape = Mock(ID=None, begin_x=None, begin_y=None, end_x=None, end_y=None)

        # WHEN the connector is created
        strategy = CreateConnectorByLineCoordinates()
        diagram_connector = strategy.create_connector(shape)

        # THEN no diagram is returned
        assert not diagram_connector
