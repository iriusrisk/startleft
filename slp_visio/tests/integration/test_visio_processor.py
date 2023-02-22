from pytest import mark

from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import validate_and_compare_otm, validate_and_compare
from slp_visio.slp_visio.visio_processor import VisioProcessor
from slp_visio.tests.resources import test_resource_paths
from slp_visio.tests.resources.test_resource_paths import expected_aws_shapes, expected_simple_boundary_tzs, \
    expected_overlapped_boundary_tzs, \
    expected_visio_boundary_and_component_tzs, expected_visio_generic_shapes, expected_visio_self_pointing_connectors, \
    expected_visio_extraneous_elements, \
    expected_visio_boundary_tz_and_default_tz, expected_visio_multiple_pages_diagram, \
    expected_visio_aws_with_tz_and_vpc, expected_visio_orphan_dataflows, expected_visio_bidirectional_connectors, \
    expected_visio_modified_single_connectors, visio_nested_tzs, expected_visio_nested_tzs, default_visio_mapping, \
    visio_nested_tzs_inside_component, expected_visio_nested_tzs_inside_component


class TestVisioProcessor:

    @mark.parametrize('vsdx,mapping', [
        (test_resource_paths.visio_aws_shapes, test_resource_paths.empty_mapping),
        (test_resource_paths.visio_empty, test_resource_paths.default_visio_mapping),
        (test_resource_paths.visio_empty, test_resource_paths.default_visio_mapping_legacy),
        (test_resource_paths.visio_empty, test_resource_paths.empty_mapping)
    ])
    def test_empties(self, vsdx, mapping):
        visio_file = open(vsdx, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 0
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_aws_shapes(self, mapping):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(mapping)],
        ).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_aws_shapes, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.custom_vpc_mapping,
        test_resource_paths.custom_vpc_mapping_legacy,
    ])
    def test_generic_elements(self, mapping):
        visio_file = open(test_resource_paths.visio_generic_shapes, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_generic_shapes, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.custom_vpc_mapping,
        test_resource_paths.custom_vpc_mapping_legacy,
    ])
    def test_self_pointing_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_self_pointing_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_self_pointing_connectors, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_extraneous_elements(self, mapping):
        visio_file = open(test_resource_paths.visio_extraneous_elements, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_extraneous_elements, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_simple_boundary_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_simple_boundary_tzs, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_simple_boundary_tzs, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_boundary_tz_and_default_tz(self, mapping):
        visio_file = open(test_resource_paths.visio_boundary_tz_and_default_tz, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_boundary_tz_and_default_tz, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_overlapped_boundary_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_overlapped_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(mapping)],
        ).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_overlapped_boundary_tzs, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_visio_boundary_and_component_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_boundary_and_component_tzs, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_boundary_and_component_tzs, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_multiple_pages_diagram(self, mapping):
        visio_file = open(test_resource_paths.visio_multiple_pages_diagram, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_multiple_pages_diagram, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_complex_diagram(self, mapping):
        visio_file = open(test_resource_paths.visio_aws_with_tz_and_vpc, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_aws_with_tz_and_vpc, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_prune_orphan_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_orphan_dataflows, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_orphan_dataflows, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_bidirectional_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_bidirectional_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_bidirectional_connectors, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_manually_modified_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_modified_single_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), expected_visio_modified_single_connectors, None)
        assert result == expected

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

        result, expected = validate_and_compare(otm, expected, None)
        assert result == expected

    @mark.parametrize('vsdx,expected', [
        (visio_nested_tzs, expected_visio_nested_tzs),
        (visio_nested_tzs_inside_component, expected_visio_nested_tzs_inside_component)
    ])
    def test_nested_trust_zones(self, vsdx, expected):
        # Given the visio file
        visio_file = open(vsdx, "r")

        # When we process it
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(default_visio_mapping)],
        ).process()

        # Then the otm should be the expected
        result, expected = validate_and_compare(otm, expected, None)
        assert result == expected

    @mark.parametrize('mapping', [
        test_resource_paths.master_unique_id_mapping_without_curly_braces,
        test_resource_paths.master_unique_id_mapping_with_curly_braces,
    ])
    def test_master_unique_id(self, mapping):
        visio_file = open(test_resource_paths.master_unique_id, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()
        result, expected = validate_and_compare_otm(otm.json(), test_resource_paths.expected_master_unique_id, None)
        assert result == expected