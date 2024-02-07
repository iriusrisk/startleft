from unittest.mock import patch, MagicMock

import pytest

from sl_util.sl_util import secure_regex as re
from sl_util.sl_util.file_utils import get_byte_data
from slp_abacus.slp_abacus.validate.abacus_validator import AbacusValidator
from slp_abacus.tests.resources.test_resource_paths import wrong_root_abacus, wrong_mxcell_abacus, wrong_mxfile_abacus, \
    wrong_mxgraphmodel_abacus, not_xml, abacus_merged
from slp_base import DiagramFileNotValidError, CommonError

filename_pattern = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\\.[abacus|xml]')


def create_mock_file(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


class TestAbacusValidator:

    @pytest.mark.parametrize('size_value', [
        pytest.param(9, id="less than expected min"),
        pytest.param((10 * 1024 * 1024) + 1, id="more than expected max")
    ])
    def test_invalid_sizes(self, size_value: int):
        # GIVEN the validator with an invalid size
        validator = AbacusValidator(create_mock_file(size_value))

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Provided diag_file is not valid. Invalid size'

    @patch('slp_abacus.slp_abacus.validate.abacus_validator.get_file_type_by_content')
    @pytest.mark.parametrize('mime', [
        'application/zip', 'application/pdf', 'text/html'
    ])
    def test_invalid_mimetype(self, mock_content_type, mime):
        # GIVEN the validator with a valid size
        file = MagicMock()
        file.__len__.return_value = 10

        # AND different types
        mock_content_type.return_value = mime

        # AND the validator
        validator = AbacusValidator(file)

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Invalid content type for diag_file'

    @pytest.mark.parametrize('mime, size, filepath', [
        pytest.param('application/octet-stream', 10, abacus_merged, id='encoded-tiny-binary'),
        pytest.param('application/json', 10 * 1024 * 1024, abacus_merged, id='xml-big-xml'),
        pytest.param('text/plain', 10 * 1024 * 1024, abacus_merged, id='encoded-big-text')
    ])
    def test_valid_file(self, mime: str, size: int, filepath: str):
        # GIVEN the valid file
        file = get_byte_data(filepath)

        # AND the validator
        validator = AbacusValidator(file)

        # WHEN we validate
        # THEN no CommonError is raised
        try:
            validator.validate()
        except CommonError:
            assert False
