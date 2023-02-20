from unittest.mock import patch, MagicMock

import pytest

from slp_base import DiagramFileNotValidError
from slp_visio.slp_visio.validate.visio_validator import VisioValidator


class TestVisioValidator:
    validator = VisioValidator(MagicMock(name="file_name"))

    @patch("os.path.getsize")
    @pytest.mark.parametrize('size_value', [
        pytest.param(9, id="less than expected min"),
        pytest.param(11 * 1024 * 1024, id="more than expected max")
    ])
    def test_invalid_sizes(self, getsize_mock, size_value):
        getsize_mock.return_value = size_value
        
        with pytest.raises(DiagramFileNotValidError) as error_info:
            self.validator.validate()

        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Provided visio file is not valid. Invalid size'

    @patch("magic.Magic.from_file")
    @patch("os.path.getsize")
    @pytest.mark.parametrize('mime_type_value', [
        pytest.param('application/zip', id="zip file")
    ])
    def test_invalid_mimetype(self, getsize_mock, get_mime_type, mime_type_value):
        getsize_mock.return_value = 20
        get_mime_type.return_value = mime_type_value

        with pytest.raises(DiagramFileNotValidError) as error_info:
            self.validator.validate()

        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Invalid content type for diag_file'

    @patch("magic.Magic.from_file")
    @patch("os.path.getsize")
    @pytest.mark.parametrize('size_value, mime_type_value', [
        pytest.param(10, 'application/vnd.ms-visio.drawing.main+xml', id="visio drawing"),
        pytest.param(10 * 1024 * 1024, 'application/octet-stream', id="octet-stream"),
    ])
    def test_valid_file(self, getsize_mock, get_mime_type, size_value, mime_type_value):
        getsize_mock.return_value = size_value
        get_mime_type.return_value = mime_type_value

        self.validator.validate()
