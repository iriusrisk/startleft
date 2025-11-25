import json
from unittest.mock import patch

import pytest
from pytest import mark, param
from sl_util.sl_util.file_utils import get_byte_data
from sl_util.tests.util.file_utils import generate_temporary_file
from slp_base.slp_base.errors import SourceFileNotValidError, MappingFileNotValidError, ErrorCode
from slp_base.slp_base.mapping import MAX_SIZE as MAPPING_MAX_SIZE, MIN_SIZE as MAPPING_MIN_SIZE
from slp_base.tests.util.otm import validate_and_compare
from slp_mtmt import MTMTProcessor
from slp_mtmt.slp_mtmt.mtmt_validator import MIN_SIZE as FILE_MIN_SIZE, MAX_SIZE as FILE_MAX_SIZE
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import model_mtmt_mvp_otm, missing_position_otm, \
    nested_trustzones_tm7, nested_trustzones_otm, nested_trustzones_line_otm, nested_trustzones_line_tm7

SAMPLE_ID = 'example-project'
SAMPLE_NAME = 'Example Project'
SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mapping_mtmt_mvp
SAMPLE_VALID_MAPPING_MVP_LEGACY_FILE = test_resource_paths.mapping_mtmt_mvp_legacy
SAMPLE_VALID_MAPPING_MVP_NO_TYPE_FILE = test_resource_paths.mapping_mtmt_mvp_no_type
DEFAULT_MAPPING_FILE = test_resource_paths.mtmt_default_mapping
MTMT_MISSING_POSITION = test_resource_paths.missing_position
MTMT_EXAMPLE_POSITION = test_resource_paths.example_position_tm7
OTM_EXAMPLE_POSITION = test_resource_paths.example_position_otm
MTMT_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_tm7
OTM_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_otm
MTMT_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_tm7
OTM_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_otm
SAMPLE_UNMAPPED_TRUSTZONES = test_resource_paths.unmapped_trustzones_tm7
SAMPLE_UNMAPPED_TRUSTZONES_OTM = test_resource_paths.unmapped_trustzones_otm
SAMPLE_MODEL_NO_NAME_FIGURES = test_resource_paths.model_with_no_name_figures_tm7
MTMT_AZURE_COMPONENTS = test_resource_paths.azure_components_tm7
OTM_AZURE_COMPONENTS = test_resource_paths.azure_components_otm
MTMT_SIMPLE_LINE_BOUNDARY = test_resource_paths.simple_line_boundary_tm7
MTMT_MULTIPLE_TRUSTZONES_SAME_TYPE = test_resource_paths.multiple_trustzones_same_type_tm7
MAPPING_MULTIPLE_TRUSTZONES_SAME_TYPE = test_resource_paths.multiple_trustzones_same_type_mapping

class TestMtmtProcessor:
    excluded_regex = [
        r"root\['components'\]\[.+?\]\['threats'\]",
        r"root\['threats'\]",
        r"root\['mitigations'\]"
    ]

    @mark.parametrize('mapping_file',
      [SAMPLE_VALID_MAPPING_FILE, SAMPLE_VALID_MAPPING_MVP_LEGACY_FILE, SAMPLE_VALID_MAPPING_MVP_NO_TYPE_FILE])
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
        (MTMT_EXAMPLE_1ORPHAN, OTM_EXAMPLE_1ORPHAN),
        (nested_trustzones_tm7, nested_trustzones_otm),
        (nested_trustzones_line_tm7, nested_trustzones_line_otm)
    ])
    def test_otm_output_of_valid_mtmt(self, source, expected):
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

    def test_unmapped_trust_zones(self):
        # GIVEN a valid MTMT file
        source_file = get_byte_data(SAMPLE_UNMAPPED_TRUSTZONES)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # AND the expected OTM
        expected_otm = json.loads(get_byte_data(SAMPLE_UNMAPPED_TRUSTZONES_OTM))

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # AND we get the json OTM
        otm_json = otm.json()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm_json, expected_otm, self.excluded_regex)
        assert result == expected

    def test_model_with_no_name_figures(self):
        # GIVEN a valid MTMT file
        source_file = get_byte_data(SAMPLE_MODEL_NO_NAME_FIGURES)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        assert len(otm.trustzones) == 3
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 3

    @mark.parametrize('source_file', [
        param(generate_temporary_file(FILE_MIN_SIZE - 1), id='mtmt file too small'),
        param(generate_temporary_file(FILE_MAX_SIZE + 1), id='mtmt file too big')
    ])
    def test_invalid_file_size(self, source_file: bytes):
        # GIVEN a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # WHEN MTMTProcessor::process is invoked
        # THEN a SourceFileNotValidError is raised
        with pytest.raises(SourceFileNotValidError) as error:
            MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # AND whose information is right
        assert error.value.title == 'Microsoft Threat Modeling Tool file is not valid'
        assert error.value.message == 'Provided source_file is not valid. Invalid size'

    @mark.parametrize('mappings', [
        param([generate_temporary_file(MAPPING_MIN_SIZE - 1)], id='default mapping file too small'),
        param([generate_temporary_file(MAPPING_MAX_SIZE + 1)], id='default mapping file too big')
    ])
    def test_invalid_mapping_file_size(self, mappings: list[bytes]):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(SAMPLE_VALID_MTMT_FILE)

        # WHEN MTMTProcessor::process is invoked
        # THEN a MappingFileNotValidError is raised
        with pytest.raises(MappingFileNotValidError) as error:
            MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, mappings).process()

        # AND the error details are correct
        assert ErrorCode.MAPPING_FILE_NOT_VALID == error.value.error_code
        assert 'Mapping files are not valid' == error.value.title
        assert 'Mapping files are not valid. Invalid size' == error.value.detail
        assert 'Mapping files are not valid. Invalid size' == error.value.message

    def test_run_azure_components(self):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(MTMT_AZURE_COMPONENTS)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        result, expected = validate_and_compare(otm.json(), OTM_AZURE_COMPONENTS, None)
        assert result == expected

    def test_run_simple_line_boundary(self):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(MTMT_SIMPLE_LINE_BOUNDARY)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        assert len(otm.trustzones) == 2
        assert otm.trustzones[0].id == 'ef4b8d94-ff80-419b-b590-b1a6aad88408'
        assert otm.trustzones[0].name == 'Generic Trust Line Boundary'
        assert otm.trustzones[0].type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[0].trustrating == 10
        assert otm.trustzones[1].id == '185f1c6f-3879-464c-89c9-dc6f0b0c2b21'
        assert otm.trustzones[1].name == 'Default trustzone'
        assert otm.trustzones[1].type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert otm.trustzones[1].trustrating == 10
        assert otm.components[0].parent == '185f1c6f-3879-464c-89c9-dc6f0b0c2b21'
        assert otm.components[1].parent == 'ef4b8d94-ff80-419b-b590-b1a6aad88408'
        assert otm.components[2].parent == '185f1c6f-3879-464c-89c9-dc6f0b0c2b21'
        assert otm.components[3].parent == '185f1c6f-3879-464c-89c9-dc6f0b0c2b21'

    def test_run_multiple_trustzones_same_type(self):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(MTMT_MULTIPLE_TRUSTZONES_SAME_TYPE)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(MAPPING_MULTIPLE_TRUSTZONES_SAME_TYPE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN we check the result is as expected
        assert len(otm.trustzones) == 5
        assert otm.trustzones[0].id == '06de5005-eca7-41c8-8848-9d942dc7994d'
        assert otm.trustzones[0].name == 'Local User Zone'
        assert otm.trustzones[0].type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm.trustzones[0].trustrating == 10
        assert otm.trustzones[1].id == '1c5a9402-2016-4bc6-9861-9e7eaf725ae6'
        assert otm.trustzones[1].name == 'Azure Trust Boundary'
        assert otm.trustzones[1].type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm.trustzones[1].trustrating == 10
        assert otm.trustzones[2].id == '871dde5d-cd57-4436-a07d-a73f039511a2'
        assert otm.trustzones[2].name == 'Azure Trust Boundary'
        assert otm.trustzones[2].type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert otm.trustzones[2].trustrating == 10
        assert otm.trustzones[3].id == 'efb356d5-0b83-4b16-be28-0337c29a7d4a'
        assert otm.trustzones[3].name == 'Remote User Zone'
        assert otm.trustzones[3].type == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert otm.trustzones[3].trustrating == 10
        assert otm.trustzones[4].id == 'b39375e4-1903-4c20-bf8d-fbfdde6d2d77'
        assert otm.trustzones[4].name == 'Remote User Zone'
        assert otm.trustzones[4].type == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert otm.trustzones[4].trustrating == 10
