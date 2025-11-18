import pytest
from pytest import mark, param
from sl_util.sl_util.file_utils import get_byte_data
from sl_util.tests.util.file_utils import generate_temporary_file
from slp_abacus import AbacusProcessor
from slp_abacus.slp_abacus.validate.abacus_validator import MAX_SIZE, MIN_SIZE
from slp_abacus.tests.resources import test_resource_paths
from slp_base import LoadingDiagramFileError
from slp_base.slp_base.errors import ErrorCode, DiagramFileNotValidError

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_FILE_INVALID_FORMAT = test_resource_paths.abacus_bad_file_format
SAMPLE_FILE_INVALID_EXTENSION = test_resource_paths.abacus_bad_file_extension
SAMPLE_DEFAULT_MAPPING = test_resource_paths.abacus_default_mapping

class TestAbacusProcessor:
    def test_no_abacus_file_format(self):
        # GIVEN a valid ABACUS file
        abacus_file = open(SAMPLE_FILE_INVALID_FORMAT, 'rb')

        # AND a valid default mapping file
        default_mapping_file = get_byte_data(SAMPLE_DEFAULT_MAPPING)

        # WHEN ABACUS is processing
        # THEN raises LoadingDiagramFileError
        with pytest.raises(LoadingDiagramFileError) as error:
            AbacusProcessor(SAMPLE_ID, SAMPLE_NAME, abacus_file, [default_mapping_file]).process()

        # AND the error details are correct
        assert ErrorCode.DIAGRAM_LOADING_ERROR == error.value.error_code
        assert "Source file cannot be loaded" == error.value.title
        assert "JSONDecodeError" == error.value.detail
        assert "Expecting value: line 1 column 1 (char 0)" == error.value.message

    @mark.parametrize('source', [
        param(generate_temporary_file(MIN_SIZE - 1, "test_min_size.txt"), id='file too small'),
        param(generate_temporary_file(MAX_SIZE + 1, "test_max_size.txt"), id='file too big')])
    def test_abacus_file_sizes(self, source):
        # GIVEN a valid default mapping file
        default_mapping_file = get_byte_data(SAMPLE_DEFAULT_MAPPING)

        # WHEN ABACUS is processing
        # THEN raises DiagramFileNotValidError
        with pytest.raises(DiagramFileNotValidError) as error:
            AbacusProcessor(SAMPLE_ID, SAMPLE_NAME, source, [default_mapping_file]).process()

        # AND the error details are correct
        assert ErrorCode.DIAGRAM_NOT_VALID == error.value.error_code
        assert "Abacus file is not valid" == error.value.title
        assert "Provided diag_file is not valid. Invalid size" == error.value.detail
        assert "Provided diag_file is not valid. Invalid size" == error.value.message

    def test_no_abacus_valid_extension(self):
        # GIVEN a valid ABACUS file
        abacus_file = open(SAMPLE_FILE_INVALID_EXTENSION, 'rb')

        # AND a valid default mapping file
        default_mapping_file = get_byte_data(SAMPLE_DEFAULT_MAPPING)

        # WHEN ABACUS is processing
        # THEN raises DiagramFileNotValidError
        with pytest.raises(DiagramFileNotValidError) as error:
            AbacusProcessor(SAMPLE_ID, SAMPLE_NAME, abacus_file, [default_mapping_file]).process()

        # AND the error details are correct
        assert ErrorCode.DIAGRAM_NOT_VALID == error.value.error_code
        assert "Abacus file is not valid" == error.value.title
        assert "Invalid content type for diag_file" == error.value.detail
        assert "Invalid content type for diag_file" == error.value.message
