import json
from unittest.mock import patch

from pytest import mark

from sl_util.sl_util.file_utils import get_byte_data
from slp_base.tests.util.otm import validate_and_compare
from slp_mtmt import MTMTProcessor
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import mapping_mtmt_mvp_legacy, mapping_mtmt_mvp_no_type, \
    model_mtmt_mvp_otm, missing_position_otm, nested_trustzones_tm7, nested_trustzones_otm, nested_trustzones_line_otm, \
    nested_trustzones_line_tm7

SAMPLE_ID = 'example-project'
SAMPLE_NAME = 'Example Project'
SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mapping_mtmt_mvp
DEFAULT_MAPPING_FILE = test_resource_paths.mtmt_default_mapping
MTMT_MISSING_POSITION = test_resource_paths.missing_position
MTMT_EXAMPLE_POSITION = test_resource_paths.example_position_tm7
OTM_EXAMPLE_POSITION = test_resource_paths.example_position_otm
MTMT_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_tm7
OTM_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_otm
MTMT_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_tm7
OTM_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_otm


class TestMtmtProcessor:
    excluded_regex = [
        r"root\['components'\]\[.+?\]\['threats'\]",
        r"root\['threats'\]",
        r"root\['mitigations'\]"
    ]

    @mark.parametrize('mapping_file', [SAMPLE_VALID_MAPPING_FILE, mapping_mtmt_mvp_legacy, mapping_mtmt_mvp_no_type])
    def test_run_valid_mappings(self, mapping_file):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(SAMPLE_VALID_MTMT_FILE)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm.json(), model_mtmt_mvp_otm, None)
        assert result == expected


    @patch('slp_base.slp_base.otm_validator.OTMValidator.validate')
    def test_run_some_missing_source_coordinates(self, validate):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(MTMT_MISSING_POSITION)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # AND we avoid the otm validation
        validate.side_effect = None

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm.json(), missing_position_otm, None)
        assert result == expected


    @mark.parametrize('source, expected', [
        (MTMT_EXAMPLE_POSITION, OTM_EXAMPLE_POSITION),
        (MTMT_EXAMPLE_1LINE, OTM_EXAMPLE_1LINE),
        (MTMT_EXAMPLE_1ORPHAN, OTM_EXAMPLE_1ORPHAN)
    ])
    def test_coordinates_borders(self, source, expected):
        # GIVEN a valid MTMT file
        source_file = get_byte_data(source)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # AND the expected OTM
        expected_otm = json.loads(get_byte_data(expected))

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # AND we get the json OTM
        otm_json = otm.json()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm_json, expected_otm, self.excluded_regex)
        assert result == expected

    @mark.parametrize('source,expected', [
        (nested_trustzones_tm7, nested_trustzones_otm),
        (nested_trustzones_line_tm7, nested_trustzones_line_otm)
    ])
    def test_nested_trust_zones(self, source, expected):
        # GIVEN a valid MTMT file
        source_file = get_byte_data(source)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # AND the expected OTM
        expected_otm = json.loads(get_byte_data(expected))

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # AND we get the json OTM
        otm_json = otm.json()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm_json, expected_otm, self.excluded_regex)
        assert result == expected