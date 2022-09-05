import pytest
from shapely.geometry import Polygon

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits
from slp_visio.slp_visio.load.representation.visio.zone_component_representer import ZoneComponentRepresenter
from slp_visio.tests.util.visio import read_shape_by_name
from tests.resources.test_resource_paths import visio_boundaries

X_FLOOR = 0
X_TOP = 10
Y_FLOOR = 0
Y_TOP = 10
DIAGRAM_LIMITS = DiagramLimits([(X_FLOOR, Y_FLOOR), (X_TOP, Y_TOP)])

BOUNDARY_TEST_FILE = visio_boundaries


class TestZoneComponentRepresenter:

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('UPPER QUADRANT', Polygon([(X_FLOOR, 7.1529), (X_FLOOR, Y_TOP), (X_TOP, Y_TOP), (X_TOP, 7.1529)])),
                              ('LOWER QUADRANT', Polygon([(X_FLOOR, Y_FLOOR), (X_FLOOR, 1.1198), (X_TOP, 1.1198), (X_TOP, Y_FLOOR)]))])
    def test_horizontal_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an horizontal oriented arc Visio shape
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = ZoneComponentRepresenter(DIAGRAM_LIMITS).build_representation(shape)

        # THEN A rectangle of the upper or lower quadrant of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('LEFT QUADRANT', Polygon([(X_FLOOR, Y_FLOOR), (X_FLOOR, Y_TOP), (1.2198, Y_TOP), (1.2198, Y_FLOOR)])),
                              ('RIGHT QUADRANT', Polygon([(9.6283, Y_FLOOR), (9.6283, Y_TOP), (X_TOP, Y_TOP), (X_TOP, Y_FLOOR)]))])
    def test_vertical_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN a vertical oriented arc Visio shape
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = ZoneComponentRepresenter(DIAGRAM_LIMITS).build_representation(shape)

        # THEN A rectangle of the left-handed or right-handed quadrant of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('UPPER LEFT TRIANGLE', Polygon([(X_FLOOR, Y_TOP), (X_FLOOR, 4.737783361351438), (3.1559753173264475, Y_TOP)])),
                              ('UPPER RIGHT TRIANGLE', Polygon([(6.141792074205819, Y_TOP), (X_TOP, Y_TOP), (X_TOP, 6.572240006247166)])),
                              ('LOWER LEFT TRIANGLE', Polygon([(X_FLOOR, Y_FLOOR), (X_FLOOR, 2.6479384916849664), (2.8076726658134796, Y_FLOOR)])),
                              ('LOWER RIGHT TRIANGLE', Polygon([(8.48168544854066, Y_FLOOR), (X_TOP, Y_FLOOR), (X_TOP, 1.7455231482858737)]))])
    def test_triangular_corner_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an arc shape oriented to a corner of the diagram
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = ZoneComponentRepresenter(DIAGRAM_LIMITS).build_representation(shape)

        # THEN A triangle with the corner of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('LEFT POLYGON', Polygon([(X_FLOOR, Y_FLOOR), (4.431528613780164, Y_FLOOR), (9.700881475100427, Y_TOP), (X_FLOOR, Y_TOP)])),
                              ('RIGHT POLYGON', Polygon([(3.110920675980997, Y_FLOOR), (X_TOP, Y_FLOOR), (X_TOP, Y_TOP), (8.451514681301747, Y_TOP)]))])
    def test_polygonal_sloped_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an arc shape slightly sloped to the diagram corner
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = ZoneComponentRepresenter(DIAGRAM_LIMITS).build_representation(shape)

        # THEN A polygon with the corner of the diagram is returned
        assert actual_representation == expected_representation
