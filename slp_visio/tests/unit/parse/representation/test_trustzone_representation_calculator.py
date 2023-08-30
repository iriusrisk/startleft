from unittest.mock import MagicMock, Mock, patch

from slp_visio.slp_visio.parse.representation import trustzone_representation_calculator
from slp_visio.slp_visio.parse.representation.trustzone_representation_calculator import \
    TrustZoneRepresentationCalculator, _get_trustzone_components, calculate_missing_trustzones_representations

MODULE_NAME = trustzone_representation_calculator.__name__

REPRESENTATION_ID = 'representation_id'
TZ_REPRESENTATION = Mock()
TZ_REPRESENTATION.id = 'tz-id-representation'
TZ_REPRESENTATION.name = 'tz-name Representation'
TZ_REPRESENTATION.position = {'x': 70, 'y': 70}
TZ_REPRESENTATION.size = {'width': 210, 'height': 210}


def mock_trustzone():
    __tz_without_representation = Mock()
    __tz_without_representation.id = 'tz-id'
    __tz_without_representation.name = 'tz-name'
    __tz_without_representation.representations = None

    return __tz_without_representation


def mock_component(start_position: int = 100):
    return MagicMock(
        representations=[
            MagicMock(
                position={'x': start_position, 'y': start_position},
                size={'width': 50, 'height': 50}
            )
        ]
    )


class TestTrustZoneRepresentationCalculator:

    @patch(f'{MODULE_NAME}.{TrustZoneRepresentationCalculator.__name__}', autospec=True)
    def test_calculate_missing_trustzones_representations(self, trustzone_calculator_mock):
        # GIVEN a trustzone without representation and some mocked components inside
        trustzone_without_representation = mock_trustzone()
        trustzone_components = [Mock(), Mock()]

        # AND a trustzone with representation
        trustzone_with_representation = mock_trustzone()
        trustzone_with_representation.representations = [TZ_REPRESENTATION]

        # AND an OTM with those trustzones and components
        otm = MagicMock(
            trustzones=[trustzone_without_representation, trustzone_with_representation],
            components=trustzone_components
        )

        # WHEN the method trustzone_representation_calculator::calculate_tz_representation is invoked
        with patch(f'{MODULE_NAME}.{_get_trustzone_components.__name__}',
                   return_value=trustzone_components) as get_trustzone_components_mock:
            calculate_missing_trustzones_representations(otm, REPRESENTATION_ID)

        # THEN the components are retrieved for the trustzone_without_representation
        get_trustzone_components_mock.assert_called_with(trustzone_without_representation.id, trustzone_components)

        # AND the trustzone representation is calculated for the trustzone_without_representation
        trustzone_calculator_mock.assert_called_with(REPRESENTATION_ID,
                                                     trustzone_without_representation,
                                                     trustzone_components)

        # AND the representation is not calculated for the trustzone that already has a representation
        assert get_trustzone_components_mock.call_count == 1
        assert trustzone_calculator_mock.return_value.calculate.call_count == 1

    def test_calculate_tz_representation_by_components(self):
        # GIVEN a trustzone without representation
        trustzone = mock_trustzone()

        # AND two components inside the trustzone
        tz_component_1 = mock_component(start_position=100)
        tz_component_2 = mock_component(start_position=200)
        trustzone_components = [tz_component_1, tz_component_2]

        # WHEN TrustZoneRepresentationCalculator::calculate is invoked
        TrustZoneRepresentationCalculator(REPRESENTATION_ID, trustzone, trustzone_components).calculate()

        # THEN the TrustZone representation is as expected
        representation = trustzone.representations[0]
        assert representation.representation == REPRESENTATION_ID
        assert representation.id == TZ_REPRESENTATION.id
        assert representation.name == TZ_REPRESENTATION.name
        assert representation.position == TZ_REPRESENTATION.position
        assert representation.size == TZ_REPRESENTATION.size

        # AND the representations of the components are made relative
        assert tz_component_1.representations[0].position['x'] == 30
        assert tz_component_1.representations[0].position['y'] == 30
        assert tz_component_2.representations[0].position['x'] == 130
        assert tz_component_2.representations[0].position['y'] == 130

    def test_calculate_tz_representation_by_components_without_representation(self):
        # GIVEN a trustzone without representation
        trustzone = mock_trustzone()

        # AND a list of components without representations
        trustzone_components = [MagicMock(representations=[]), MagicMock()]

        # WHEN the method TrustZoneRepresentationCalculator::calculate is invoked
        TrustZoneRepresentationCalculator(REPRESENTATION_ID, trustzone, trustzone_components).calculate()

        # THEN no representation is calculated
        assert not trustzone.representations
