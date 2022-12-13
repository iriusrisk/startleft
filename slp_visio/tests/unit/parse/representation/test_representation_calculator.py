from pytest import mark
from shapely.geometry import Polygon, box

from otm.otm.otm import RepresentationElement
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits, DiagramComponent, DiagramComponentOrigin
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator

DIAGRAM_REPRESENTATION_ID = 'diagram_representation_id'
DIAGRAM_LIMITS = DiagramLimits([(0, 0), (15, 15)])

COMPONENT_ID = 'component-id'
COMPONENT_NAME = 'component-name'

FIRST_LEVEL_POLYGON = box(1, 4, 12, 14)
SECOND_LEVEL_POLYGON = box(4, 6, 11, 11)
THIRD_LEVEL_POLYGON = box(5, 7, 9, 9)

representation_calculator = RepresentationCalculator(DIAGRAM_REPRESENTATION_ID, DIAGRAM_LIMITS)


def create_component(
        origin: DiagramComponentOrigin = DiagramComponentOrigin.SIMPLE_COMPONENT,
        parent: DiagramComponent = None,
        trustzone: bool = False,
        representation: Polygon= None,
) -> DiagramComponent:
    return DiagramComponent(
        id=COMPONENT_ID,
        name=COMPONENT_NAME,
        type='component-type',
        origin=origin,
        parent=parent,
        trustzone=trustzone,
        representation=representation
    )


def create_representation(xy: (), wh: ()) -> RepresentationElement:
    return RepresentationElement(
        id_=f'{COMPONENT_ID}-representation',
        name=f'{COMPONENT_NAME} Representation',
        representation=DIAGRAM_REPRESENTATION_ID,
        position={'x': xy[0], 'y': xy[1]},
        size={'width': wh[0], 'height': wh[1]}
    )


class TestRepresentationCalculator:

    @mark.parametrize('parent,expected_representation', [
        (create_component(representation=FIRST_LEVEL_POLYGON, trustzone=True), create_representation((4, 6), (4, 2))),
        (create_component(representation=SECOND_LEVEL_POLYGON, trustzone=False), create_representation((1, 2), (4, 2)))
    ])
    def test_component_with_parent(self, parent, expected_representation):
        # GIVEN a diagram component representing an OTM Component with parent
        component = create_component(
            trustzone=False,
            parent=parent,
            representation=THIRD_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN a representation element with RELATIVE coordinates and size is calculated
        assert representation == expected_representation

    def test_component_without_parent(self):
        # GIVEN a diagram component representing an OTM Component WITHOUT parent
        component = create_component(
            trustzone=False,
            parent=None,
            representation=THIRD_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    def test_component_with_boundary_trustzone_parent(self):
        # GIVEN a boundary TrustZone as parent
        parent = create_component(
            origin=DiagramComponentOrigin.BOUNDARY,
            representation=FIRST_LEVEL_POLYGON,
            trustzone=True)

        # AND a diagram component representing an OTM Component with that parent
        component = create_component(
            trustzone=False,
            parent=parent,
            representation=THIRD_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    @mark.parametrize('parent,expected_representation', [
        (create_component(representation=FIRST_LEVEL_POLYGON, trustzone=True), create_representation((3, 3), (7, 5))),
        (create_component(representation=FIRST_LEVEL_POLYGON, trustzone=False), create_representation((3, 3), (7, 5)))
    ])
    def test_trustzone_with_parent(self, parent, expected_representation):
        # GIVEN a diagram component representing an OTM TrustZone with parent
        trustzone = create_component(
            trustzone=True,
            parent=parent,
            representation=SECOND_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN a representation element with RELATIVE coordinates and the right size is calculated
        assert representation == expected_representation

    def test_trustzone_with_boundary_trustzone_parent(self):
        # GIVEN a boundary TrustZone as parent
        parent = create_component(
            origin=DiagramComponentOrigin.BOUNDARY,
            representation=FIRST_LEVEL_POLYGON,
            trustzone=True)

        # AND a diagram component representing an OTM TrustZone with that parent
        trustzone = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            representation=SECOND_LEVEL_POLYGON,
            trustzone=True
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN no representation is returned
        assert representation is None

    def test_boundary_trustzone_without_parent(self):
        # GIVEN a diagram component representing an OTM TrustZone WITHOUT parent
        trustzone = create_component(
            origin=DiagramComponentOrigin.BOUNDARY,
            trustzone=True,
            parent=None,
            representation=FIRST_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN no representation is returned
        assert representation is None

    def test_simple_trustzone_without_parent(self):
        # GIVEN a diagram component representing an OTM TrustZone WITHOUT parent
        trustzone = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            trustzone=True,
            parent=None,
            representation=FIRST_LEVEL_POLYGON
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN a representation element with ABSOLUTE coordinates and the right size is calculated
        assert representation == create_representation((1, 1), (11, 10))

    @mark.parametrize('out_of_limits_polygon', [box(0, 0, 20, 15), box(0, 0, 15, 20), box(0, 0, 20, 20)])
    def test_error_component_out_of_limits(self, out_of_limits_polygon):
        # GIVEN a diagram component whose coordinates are out of the diagram limits
        component = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            representation=out_of_limits_polygon
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    @mark.parametrize('negative_coordinates_polygon', [box(-1, 0, 15, 15), box(0, -1, 15, 15)])
    def test_error_negative_coordinates(self, negative_coordinates_polygon):
        # GIVEN a diagram component whose coordinates are negative
        component = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            representation=negative_coordinates_polygon
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    @mark.parametrize('negative_dimensions_polygon', [box(0, 0, -15, 15), box(0, 0, 15, -15)])
    def test_error_negative_width_or_height(self, negative_dimensions_polygon):
        # GIVEN a diagram component whose width or length are negative
        component = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            representation=negative_dimensions_polygon
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None
