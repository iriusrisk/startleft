from unittest.mock import patch, MagicMock

import pytest
from starlette.datastructures import UploadFile, Headers

from sl_util.sl_util import secure_regex as re
from sl_util.sl_util.file_utils import get_byte_data
from sl_util.tests.util.file_utils import get_upload_file
from slp_base import DiagramFileNotValidError, CommonError
from slp_drawio.slp_drawio.validate.drawio_validator import DrawioValidator
from slp_drawio.tests.resources.test_resource_paths import wrong_mxgraphmodel_drawio, wrong_mxfile_drawio, \
    wrong_mxcell_drawio, wrong_root_drawio, aws_minimal_drawio, aws_minimal_xml, not_xml

filename_pattern = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\\.[drawio|xml]')


def create_mock_file(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


class TestDrawioValidator:

    @pytest.mark.parametrize('size_value', [
        pytest.param(9, id="less than expected min"),
        pytest.param((10 * 1024 * 1024) + 1, id="more than expected max")
    ])
    def test_invalid_sizes(self, size_value: int):
        # GIVEN the validator with an invalid size
        validator = DrawioValidator(create_mock_file(size_value))

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Provided diag_file is not valid. Invalid size'

    @patch('slp_drawio.slp_drawio.validate.drawio_validator.get_file_type_by_content')
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
        validator = DrawioValidator(file)

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Invalid content type for diag_file'

    @pytest.mark.parametrize('filepath', [
        pytest.param(wrong_root_drawio, id='wrong_root'),
        pytest.param(wrong_mxcell_drawio, id='wrong_mxcell'),
        pytest.param(wrong_mxfile_drawio, id='wrong_mxfile'),
        pytest.param(wrong_mxgraphmodel_drawio, id='wrong_mxgraphmodel'),
        pytest.param(not_xml, id='not_xml')
    ])
    def test_invalid_schema(self, filepath: str):
        # GIVEN the wrong file
        file = get_byte_data(filepath)

        # AND the validator
        validator = DrawioValidator(file)

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Provided diag_file is not valid. It does not comply with schema'

    @pytest.mark.parametrize('mime, size, filepath', [
        pytest.param('application/octet-stream', 10, aws_minimal_drawio, id='encoded-tiny-binary'),
        pytest.param('application/xml', 10 * 1024 * 1024, aws_minimal_xml, id='xml-big-xml'),
        pytest.param('text/plain', 10 * 1024 * 1024, aws_minimal_drawio, id='encoded-big-text')
    ])
    def test_valid_file(self, mime: str, size: int, filepath: str):
        # GIVEN the valid file
        file = get_byte_data(filepath)

        # AND the validator
        validator = DrawioValidator(file)

        # WHEN we validate
        # THEN no CommonError is raised
        try:
            validator.validate()
        except CommonError:
            assert False

