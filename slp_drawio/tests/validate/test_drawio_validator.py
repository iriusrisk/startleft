from unittest.mock import Mock

import pytest
from starlette.datastructures import UploadFile, Headers

from sl_util.sl_util import secure_regex as re
from slp_base import DiagramFileNotValidError, CommonError
from slp_drawio.slp_drawio.validate.drawio_validator import DrawioValidator
from slp_drawio.tests.resources.test_resource_paths import wrong_mxgraphmodel_drawio, wrong_mxfile_drawio, \
    wrong_mxcell_drawio, wrong_root_drawio, aws_minimal_drawio, aws_minimal_drawio_xml, not_xml
from slp_visio.tests.util.files import get_upload_file

filename_pattern = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\\.[drawio|xml]')


class TestDrawioValidator:

    @pytest.mark.parametrize('size_value', [
        pytest.param(9.999, id="less than expected min"),
        pytest.param(10.001 * 1024 * 1024, id="more than expected max")
    ])
    def test_invalid_sizes(self, size_value):
        # GIVEN the validator with an invalid size
        validator = DrawioValidator(Mock(size=size_value))

        # WHEN we validate
        with pytest.raises(DiagramFileNotValidError) as error_info:
            validator.validate()

        # THEN the error raised is as expected
        assert error_info.typename == 'DiagramFileNotValidError'
        assert error_info.value.message == 'Provided diag_file is not valid. Invalid size'

    @pytest.mark.parametrize('mime', [
        'application/zip', 'application/pdf', 'text/html'
    ])
    def test_invalid_mimetype(self, mime):
        # GIVEN the validator with an invalid size
        validator = DrawioValidator(Mock(content_type=mime, size=10))

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
        # GIVEN the mocked file
        file: UploadFile = get_upload_file(filepath)
        file.size = 10
        file.headers = Headers({'content-type': 'application/octet-stream'})
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
        pytest.param('application/xml', 10 * 1024 * 1024, aws_minimal_drawio_xml, id='xml-big-xml'),
        pytest.param('text/plain', 10 * 1024 * 1024, aws_minimal_drawio, id='encoded-big-text')
    ])
    def test_valid_file(self, mime: str, size: int, filepath: str):
        # GIVEN the mocked file
        file: UploadFile = get_upload_file(filepath)
        file.size = size
        file.headers = Headers({'content-type': mime})
        # AND the validator
        validator = DrawioValidator(file)

        # WHEN we validate THEN no CommonError is raised
        try:
            validator.validate()
        except CommonError:
            assert False

        # AND the filename is an uuid and the original extension
        match = filename_pattern.match(file.filename)
        assert match

    @pytest.mark.parametrize('ext', [
        pytest.param('\x1C\x00d\x08r\x7Fawio\x0D', id='control-chars'),
        pytest.param(' x\x200\x2Am\x26\x25l\x2F', id='printable-non-alpha'),
        pytest.param('0d1r2a3w4i5o90', id='numeric')
    ])
    def test_filename_sanitized(self, ext: str):
        # GIVEN the mocked file
        file: UploadFile = get_upload_file(aws_minimal_drawio)
        file.size = 10
        file.filename = f'e.xam.ple.{ext}'
        file.headers = Headers({'content-type': 'application/xml'})
        # AND the validator
        validator = DrawioValidator(file)

        # WHEN we validate
        validator.validate()

        # THEN the filename is an uuid and a valid extension
        match = filename_pattern.match(file.filename)
        assert match
