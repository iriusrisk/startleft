from pytest import mark
from shapely.geometry import Polygon, box

from otm.otm.entity.representation import RepresentationElement
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits, DiagramComponent, DiagramComponentOrigin
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator

DIAGRAM_REPRESENTATION_ID = 'diagram_representation_id'
DIAGRAM_LIMITS = DiagramLimits([(0, 0), (1.5, 1.5)])

COMPONENT_ID = 'component-id'
COMPONENT_NAME = 'component-name'

LARGER_SHAPE = box(0.1, 0.4, 1.2, 1.4)
MEDIUM_SHAPE = box(0.4, 0.6, 1.1, 1.1)
SMALL_SHAPE = box(0.5, 0.7, 0.9, 0.9)

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
        (create_component(representation=LARGER_SHAPE, trustzone=True), create_representation((66, 82), (66, 33))),
        (create_component(representation=MEDIUM_SHAPE, trustzone=False), create_representation((16, 32), (66, 33)))
    ])
    def test_component_with_parent(self, parent, expected_representation):
        # GIVEN a diagram component representing an OTM Component with parent
        component = create_component(
            trustzone=False,
            parent=parent,
            representation=SMALL_SHAPE
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
            representation=SMALL_SHAPE
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    def test_component_with_boundary_trustzone_parent(self):
        # GIVEN a boundary TrustZone as parent
        parent = create_component(
            origin=DiagramComponentOrigin.BOUNDARY,
            representation=LARGER_SHAPE,
            trustzone=True)

        # AND a diagram component representing an OTM Component with that parent
        component = create_component(
            trustzone=False,
            parent=parent,
            representation=SMALL_SHAPE
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(component)

        # THEN no representation is returned
        assert representation is None

    @mark.parametrize('parent,expected_representation', [
        (create_component(representation=LARGER_SHAPE, trustzone=True), create_representation((50, 50), (114, 82))),
        (create_component(representation=LARGER_SHAPE, trustzone=False), create_representation((50, 50), (114, 82)))
    ])
    def test_trustzone_with_parent(self, parent, expected_representation):
        # GIVEN a diagram component representing an OTM TrustZone with parent
        trustzone = create_component(
            trustzone=True,
            parent=parent,
            representation=MEDIUM_SHAPE
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN a representation element with RELATIVE coordinates and the right size is calculated
        assert representation == expected_representation

    def test_trustzone_with_boundary_trustzone_parent(self):
        # GIVEN a boundary TrustZone as parent
        parent = create_component(
            origin=DiagramComponentOrigin.BOUNDARY,
            representation=LARGER_SHAPE,
            trustzone=True)

        # AND a diagram component representing an OTM TrustZone with that parent
        trustzone = create_component(
            origin=DiagramComponentOrigin.SIMPLE_COMPONENT,
            parent=parent,
            trustzone=True,
            representation=MEDIUM_SHAPE
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
            representation=LARGER_SHAPE
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
            representation=LARGER_SHAPE
        )

        # WHEN RepresentationCalculator::calculate_representation is called
        representation = representation_calculator.calculate_representation(trustzone)

        # THEN a representation element with ABSOLUTE coordinates and the right size is calculated
        assert representation == create_representation((16, 16), (181, 164))

    @mark.parametrize('out_of_limits_polygon', [box(0, 0, 2.0, 1.5), box(0, 0, 1.5, 2.0), box(0, 0, 2.0, 2.0)])
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

    @mark.parametrize('negative_coordinates_polygon', [box(-0.1, 0, 1.5, 1.5), box(0, -0.1, 1.5, 1.5)])
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

    @mark.parametrize('negative_dimensions_polygon', [box(0, 0, -1.5, 1.5), box(0, 0, 1.5, -1.5)])
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
