from pytest import mark

from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import validate_and_diff
from slp_visio.slp_visio.visio_processor import VisioProcessor
from slp_visio.tests.resources import test_resource_paths
from slp_visio.tests.resources.test_resource_paths import expected_empty_mapping_file, expected_empty_visio_file, \
    expected_empty_mapping_and_visio_files, expected_aws_shapes, expected_generic_elements, \
    expected_self_pointing_connectors, expected_extraneous_elements, expected_simple_boundary_tzs, \
    expected_boundary_tz_and_default_tz, expected_overlapped_boundary_tzs, \
    expected_visio_boundary_and_component_tzs, expected_multiple_pages_diagram, expected_complex_diagram, \
    expected_prune_orphan_connectors, expected_bidirectional_connectors, expected_manually_modified_connectors

VALIDATION_EXCLUDED_REGEX = r"root\[\'dataflows'\]\[.+?\]\['name'\]"


class TestVisioProcessor:
    def test_empty_mapping_file(self):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.empty_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_empty_mapping_file, VALIDATION_EXCLUDED_REGEX) == {}

    def test_empty_visio_file(self):
        visio_file = open(test_resource_paths.visio_empty, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_empty_visio_file, VALIDATION_EXCLUDED_REGEX) == {}

    def test_empty_mapping_and_visio_files(self):
        visio_file = open(test_resource_paths.visio_empty, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.empty_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_empty_mapping_and_visio_files, VALIDATION_EXCLUDED_REGEX) == {}

    def test_aws_shapes(self):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_aws_shapes, VALIDATION_EXCLUDED_REGEX) == {}

    def test_generic_elements(self):
        visio_file = open(test_resource_paths.visio_generic_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.custom_vpc_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_generic_elements, VALIDATION_EXCLUDED_REGEX) == {}

    def test_self_pointing_connectors(self):
        visio_file = open(test_resource_paths.visio_self_pointing_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.custom_vpc_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_self_pointing_connectors, VALIDATION_EXCLUDED_REGEX) == {}

    def test_extraneous_elements(self):
        visio_file = open(test_resource_paths.visio_extraneous_elements, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_extraneous_elements, VALIDATION_EXCLUDED_REGEX) == {}

    def test_simple_boundary_tzs(self):
        visio_file = open(test_resource_paths.visio_simple_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_simple_boundary_tzs, VALIDATION_EXCLUDED_REGEX) == {}

    def test_boundary_tz_and_default_tz(self):
        visio_file = open(test_resource_paths.visio_boundary_tz_and_default_tz, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_boundary_tz_and_default_tz, VALIDATION_EXCLUDED_REGEX) == {}

    def test_overlapped_boundary_tzs(self):
        visio_file = open(test_resource_paths.visio_overlapped_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_overlapped_boundary_tzs, VALIDATION_EXCLUDED_REGEX) == {}

    def test_visio_boundary_and_component_tzs(self):
        visio_file = open(test_resource_paths.visio_boundary_and_component_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_visio_boundary_and_component_tzs, VALIDATION_EXCLUDED_REGEX) == {}

    def test_multiple_pages_diagram(self):
        visio_file = open(test_resource_paths.visio_multiple_pages_diagram, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_multiple_pages_diagram, VALIDATION_EXCLUDED_REGEX) == {}

    def test_complex_diagram(self):
        visio_file = open(test_resource_paths.visio_aws_with_tz_and_vpc, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping), get_data(test_resource_paths.custom_vpc_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_complex_diagram, VALIDATION_EXCLUDED_REGEX) == {}

    def test_prune_orphan_connectors(self):
        visio_file = open(test_resource_paths.visio_orphan_dataflows, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_prune_orphan_connectors, VALIDATION_EXCLUDED_REGEX) == {}

    def test_bidirectional_connectors(self):
        visio_file = open(test_resource_paths.visio_bidirectional_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_bidirectional_connectors, VALIDATION_EXCLUDED_REGEX) == {}

    def test_manually_modified_connectors(self):
        visio_file = open(test_resource_paths.visio_modified_single_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected_manually_modified_connectors, VALIDATION_EXCLUDED_REGEX) == {}

    @mark.parametrize('vsdx,expected', [
        (test_resource_paths.visio_origin_target_trustzone, test_resource_paths.expected_origin_target_trustzone),
        (test_resource_paths.visio_origin_trustzone, test_resource_paths.expected_origin_trustzone),
        (test_resource_paths.visio_target_trustzone, test_resource_paths.expected_origin_trustzone),
    ])
    def test_dataflows_connecting_trust_zones(self, vsdx, expected):
        # Given the visio file
        visio_file = open(vsdx, "r")

        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert validate_and_diff(otm, expected, None) == {}
