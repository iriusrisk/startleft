import pytest
from shapely.geometry import Polygon

from slp_visio.representation.visio.simple_component_representer import SimpleComponentRepresenter
from tests.resources.test_resource_paths import visio_simple_components
from tests.util.visio import read_shape_by_name

SIMPLE_COMPONENTS_TEST_FILE = visio_simple_components


class TestSimpleComponentRepresenter:

    @pytest.mark.parametrize('shape_name,expected_representation',
                             [('Generic rectangular', Polygon([(1.705, 4.4068), (1.705, 5.4068), (3.205, 5.4068), (3.205, 4.4068)])),
                              ('Stencil squared', Polygon([(4.7975, 5.8748), (4.7975, 6.3748), (5.2975, 6.3748), (5.2975, 5.8748)])),
                              ('Stencil custom', Polygon([(7.0222, 6.11765), (7.0222, 6.68015), (8.0222, 6.68015), (8.0222, 6.11765)])),
                              ('Generic squared', Polygon([(4.7974, 2.5241), (4.7974, 4.0241), (6.2974, 4.0241), (6.2974, 2.5241)])),
                              ('Generic triangular', Polygon([(8.1648, 4.190099999999999), (8.1648, 5.4901), (9.6648, 5.4901), (9.6648, 4.190099999999999)]))])
    def test_component_representation(self, shape_name: str, expected_representation: Polygon):
        # GIVEN an horizontal oriented arc Visio shape
        shape = read_shape_by_name(SIMPLE_COMPONENTS_TEST_FILE, shape_name)

        # WHEN building shape representation
        actual_representation = SimpleComponentRepresenter().build_representation(shape)

        # THEN A rectangle of the upper or lower quadrant of the diagram is returned
        assert actual_representation == expected_representation


