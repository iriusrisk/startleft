from unittest.mock import MagicMock

import pytest

from otm.otm.provider import Provider
from slp_base import IacType, DiagramType, EtmType, IacFileNotValidError
from slp_base.slp_base.errors import SourceFileNotValidError
from startleft.startleft.api.check_mime_type import check_mime_type


@check_mime_type('file', 'provider')
def mock_definition(**kwargs):
    return True


@check_mime_type('file', 'provider', IacFileNotValidError)
def mock_definition_with_custom_error(**kwargs):
    return True


class TestCheckMimeType:

    @pytest.mark.parametrize('content_type, provider', [
        pytest.param('application/json', IacType.CLOUDFORMATION,
                     id="valid json file for CFT"),
        pytest.param('application/octet-stream', IacType.TERRAFORM,
                     id="valid octet-stream file for TF"),
        pytest.param('application/vnd.ms-visio.drawing.main+xml', DiagramType.VISIO,
                     id="valid ms-visio file for Visio")
    ])
    def test_check_mime_type_allowed(self, content_type, provider):
        mocked_file = MagicMock(content_type=content_type)
        assert mock_definition(file=mocked_file, provider=provider)

    @pytest.mark.parametrize('content_type, provider', [
        pytest.param('application/json', EtmType.MTMT,
                     id="invalid json file for MTMT"),
        pytest.param('application/vnd.ms-visio.drawing.main+xml', IacType.TERRAFORM,
                     id="invalid ms-visio file for Terraform")
    ])
    def test_check_mime_type_disallowed(self, content_type, provider: Provider):
        mocked_file = MagicMock(filename='filename', content_type=content_type)
        with pytest.raises(SourceFileNotValidError) as error:
            mock_definition(file=mocked_file, provider=provider)

        assert error.value.error_code.http_status == 400
        assert error.typename == 'SourceFileNotValidError'
        assert error.value.title == f'Invalid {provider.provider_name} file'
        assert error.value.detail == 'Invalid content type for file filename'
        assert error.value.message == f'filename with content-type {content_type} is not valid,' \
                                      f' the valid types are {provider.valid_mime}'

    def test_custom_error(self):
        mocked_file = MagicMock(content_type='application/json')
        with pytest.raises(IacFileNotValidError) as error:
            mock_definition_with_custom_error(file=mocked_file, provider=EtmType.MTMT)

        assert error.value.error_code.http_status == 400
        assert error.typename == 'IacFileNotValidError'
