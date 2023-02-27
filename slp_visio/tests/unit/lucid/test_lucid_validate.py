from unittest.mock import patch, MagicMock, mock_open, Mock

import pytest

from slp_base import DiagramFileNotValidError
from slp_visio.slp_visio.lucid.validate.lucid_validator import LucidValidator


class MockZipf:
    def __init__(self, filename):
        self.filelist = [Mock(filename=filename)]

    def __iter__(self):
        return iter(self.filelist)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestLucidValidator:
    validator = LucidValidator(MagicMock(name="file_name"))

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
        pytest.param('application/xml', id="xml file")
    ])
    def test_invalid_mimetype(self, getsize_mock, get_mime_type, mime_type_value):
        getsize_mock.return_value = 20
        get_mime_type.return_value = mime_type_value

        with pytest.raises(DiagramFileNotValidError) as error_info:
            self.validator.validate()

        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Invalid content type for diag_file'

    @patch("slp_visio.slp_visio.validate.visio_validator.ZipFile")
    @patch("magic.Magic.from_file")
    @patch("os.path.getsize")
    @pytest.mark.parametrize('size_value, mime_type_value', [
        pytest.param(10, 'application/vnd.ms-visio.drawing.main+xml', id="visio drawing"),
        pytest.param(10 * 1024 * 1024, 'application/octet-stream', id="octet-stream"),
        pytest.param(10 * 1024 * 1024, 'application/zip', id="zip file")
    ])
    def test_valid_file(self, getsize_mock, get_mime_type, zip_file,
                        size_value, mime_type_value):
        getsize_mock.return_value = size_value
        get_mime_type.return_value = mime_type_value
        zip_file.return_value = MockZipf('[Content_Types].xml')
        zip_file.return_value.open = mock_open(read_data='')

        self.validator.validate()

    @patch("slp_visio.slp_visio.validate.visio_validator.ZipFile")
    @patch("magic.Magic.from_file")
    @patch("os.path.getsize")
    def test_invalid_zip(self, getsize_mock, get_mime_type, zip_file):
        getsize_mock.return_value = 10
        get_mime_type.return_value = 'application/zip'
        zip_file.return_value = MockZipf('invalid-file.xml')
        zip_file.return_value.open = mock_open(read_data='')

        with pytest.raises(DiagramFileNotValidError) as error_info:
            self.validator.validate()

        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Invalid content type for diag_file'
