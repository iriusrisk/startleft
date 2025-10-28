import pytest
from pytest import mark, param

from sl_util.sl_util.file_utils import get_byte_data
from sl_util.tests.util.file_utils import generate_temporary_file
from slp_base import MappingFileNotValidError
from slp_base.slp_base.errors import ErrorCode
from slp_base.slp_base.mapping import MAX_SIZE as MAPPING_MAX_SIZE, MIN_SIZE as MAPPING_MIN_SIZE
from slp_drawio import DrawioProcessor
from slp_drawio.tests.resources import test_resource_paths

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_DRAWIO_PATH = test_resource_paths.aws_minimal_xml
DEFAULT_MAPPING_FILE = get_byte_data(test_resource_paths.default_drawio_mapping)

class TestDrawioProcessor:
    @mark.parametrize('mappings', [
        param([generate_temporary_file(MAPPING_MIN_SIZE - 1), DEFAULT_MAPPING_FILE], id='mapping file too small'),
        param([generate_temporary_file(MAPPING_MAX_SIZE + 1), DEFAULT_MAPPING_FILE], id='mapping file too big'),
        param([DEFAULT_MAPPING_FILE, generate_temporary_file(MAPPING_MIN_SIZE - 1)], id='custom mapping file too small'),
        param([DEFAULT_MAPPING_FILE, generate_temporary_file(MAPPING_MAX_SIZE + 1)], id='custom mapping file too big')
    ])
    def test_invalid_mapping_size(self, mappings: list[bytes]):
        # GIVEN a valid drawio
        drawio_file = open(SAMPLE_VALID_DRAWIO_PATH, 'rb')

        # AND a mapping file with an invalid size ('mappings' arg)

        # WHEN DrawioProcessor::process is invoked
        # THEN a MappingFileNotValidError is raised
        with pytest.raises(MappingFileNotValidError) as error:
            DrawioProcessor(SAMPLE_ID, SAMPLE_NAME, drawio_file, mappings).process()

        # AND the error details are correct
        assert ErrorCode.MAPPING_FILE_NOT_VALID == error.value.error_code
        assert 'Mapping files are not valid' == error.value.title
        assert 'Mapping files are not valid. Invalid size' == error.value.detail
        assert 'Mapping files are not valid. Invalid size' == error.value.message
