import pytest
from shapely.geometry import Polygon

from startleft.diagram.representation.visio.boundary_component_representer import BoundaryComponentRepresenter
from tests.resources.test_resource_paths import visio_boundaries
from tests.util.visio import read_shape_by_name

X_LIMIT = 10
Y_LIMIT = 10

BOUNDARY_TEST_FILE = visio_boundaries


class TestBoundaryComponentRepresenter:

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('UPPER QUADRANT', Polygon([(0, 7.1529), (0, Y_LIMIT), (X_LIMIT, Y_LIMIT), (X_LIMIT, 7.1529)])),
                              ('LOWER QUADRANT', Polygon([(0, 0), (0, 1.1198), (X_LIMIT, 1.1198), (X_LIMIT, 0)]))])
    def test_horizontal_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an horizontal oriented arc Visio shape
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = BoundaryComponentRepresenter((X_LIMIT, Y_LIMIT)).build_representation(shape)

        # THEN A rectangle of the upper or lower quadrant of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('LEFT QUADRANT', Polygon([(0, 0), (0, Y_LIMIT), (1.2198, Y_LIMIT), (1.2198, 0)])),
                              ('RIGHT QUADRANT', Polygon([(9.6283, 0), (9.6283, Y_LIMIT), (X_LIMIT, Y_LIMIT), (X_LIMIT, 0)]))])
    def test_vertical_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN a vertical oriented arc Visio shape
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = BoundaryComponentRepresenter((X_LIMIT, Y_LIMIT)).build_representation(shape)

        # THEN A rectangle of the left-handed or right-handed quadrant of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('UPPER LEFT TRIANGLE', Polygon([(0, Y_LIMIT), (0, 4.737783361351438), (3.1559753173264475, Y_LIMIT)])),
                              ('UPPER RIGHT TRIANGLE', Polygon([(6.141792074205819, Y_LIMIT), (X_LIMIT, Y_LIMIT), (X_LIMIT, 6.572240006247166)])),
                              ('LOWER LEFT TRIANGLE', Polygon([(0, 0), (0, 2.6479384916849664), (2.8076726658134796, 0)])),
                              ('LOWER RIGHT TRIANGLE', Polygon([(8.48168544854066, 0), (X_LIMIT, 0), (X_LIMIT, 1.7455231482858737)]))])
    def test_triangular_corner_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an arc shape oriented to a corner of the diagram
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = BoundaryComponentRepresenter((X_LIMIT, Y_LIMIT)).build_representation(shape)

        # THEN A triangle with the corner of the diagram is returned
        assert actual_representation == expected_representation

    @pytest.mark.parametrize('arc_shape_name,expected_representation',
                             [('LEFT POLYGON', Polygon([(0, 0), (4.431528613780164, 0), (9.700881475100427, Y_LIMIT), (0, Y_LIMIT)])),
                              ('RIGHT POLYGON', Polygon([(3.110920675980997, 0), (X_LIMIT, 0), (X_LIMIT, Y_LIMIT), (8.451514681301747, Y_LIMIT)]))])
    def test_polygonal_sloped_boundary(self, arc_shape_name: str, expected_representation: Polygon):
        # GIVEN an arc shape slightly sloped to the diagram corner
        shape = read_shape_by_name(BOUNDARY_TEST_FILE, arc_shape_name)

        # WHEN building shape representation
        actual_representation = BoundaryComponentRepresenter((X_LIMIT, Y_LIMIT)).build_representation(shape)

        # THEN A polygon with the corner of the diagram is returned
        assert actual_representation == expected_representation
