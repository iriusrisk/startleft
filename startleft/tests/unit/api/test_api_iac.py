import typing
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

import startleft.startleft.api.controllers.iac.iac_create_otm_controller as controller
from otm.otm.otm_builder import OtmBuilder
from slp_base import LoadingIacFileError, IacFileNotValidError, LoadingMappingFileError, OtmBuildingError, \
    OtmGenerationError
from slp_base.slp_base.provider_type import IacType

PROJECT_ID = 'id'
PROJECT_NAME = 'name'
TESTING_IAC_TYPE = IacType.CLOUDFORMATION
OTM_SAMPLE = OtmBuilder(PROJECT_ID, PROJECT_NAME, TESTING_IAC_TYPE).build()


def mock_provider_processor_result(mock_otm_processor, mock_get_processor, result):
    mock_otm_processor.process.return_value = result
    mock_get_processor.return_value = mock_otm_processor


def mock_provider_processor_error(mock_otm_processor, mock_get_processor, error):
    mock_otm_processor.process.side_effect = error
    mock_get_processor.return_value = mock_otm_processor


class TestApiIac:

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_happy_path(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked valid file of any provider
        valid_iac_file = MagicMock(filename='valid_iac_file', content_type='application/json',
                                   file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # WHEN the POST /iac endpoint is called with iac params AND no error is raised
        mock_provider_processor_result(mock_otm_processor, mock_get_processor, OTM_SAMPLE)
        response = controller.iac(valid_iac_file, TESTING_IAC_TYPE, 'happy_path_id', 'happy_path_name',
                                  valid_mapping_file)

        # THEN a response with HTTP status 201 is returned
        assert response.status_code == 201

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_on_loading_iac_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a LoadingIacFileError
        with pytest.raises(LoadingIacFileError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = LoadingIacFileError('mocked error IAC_LOADING_ERROR', 'mocked error detail',
                                             'mocked error msg 1')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_loading_iac_error_id',
                           'iac_controller_on_loading_iac_error_name', valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the error_type in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'IAC_LOADING_ERROR'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_on_iac_file_not_valid_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND the mocked method throwing a IacFileNotValidError
        with pytest.raises(IacFileNotValidError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = IacFileNotValidError('mocked error IAC_NOT_VALID', 'mocked error detail', 'mocked error msg 2')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_iac_file_not_valid_error_id',
                           'iac_controller_on_iac_file_not_valid_error_name', valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the error_type in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'IAC_NOT_VALID'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_on_loading_mapping_file_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND the mocked method throwing a LoadingMappingFileError
        with pytest.raises(LoadingMappingFileError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = LoadingMappingFileError('mocked error MAPPING_LOADING_ERROR', 'mocked error detail',
                                                 'mocked error msg 3')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            # THEN a response HTTP Status that matches the error is returned
            controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_loading_mapping_file_error_id',
                           'iac_controller_on_loading_mapping_file_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'MAPPING_LOADING_ERROR'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_on_otm_building_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND the mocked method throwing a OtmBuildingError
        with pytest.raises(OtmBuildingError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = OtmBuildingError('mocked error OTM_BUILDING_ERROR', 'mocked error detail',
                                          'mocked error msg 4')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_otm_building_error_id',
                           'iac_controller_on_otm_building_error_name', valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the error_type in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'OTM_BUILDING_ERROR'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_on_otm_generation_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND mocked method throwing a OtmGenerationError
        with pytest.raises(OtmGenerationError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = OtmGenerationError('mocked error OTM_GENERATION_ERROR', 'mocked error detail',
                                            'mocked error msg 5')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_otm_generation_error_id',
                           'iac_controller_on_otm_generation_error_name', valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the error_type in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 500
        assert error.value.error_code.name == 'OTM_GENERATION_ERROR'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_multiple_files_happy_path(self, mock_get_processor, mock_otm_processor):
        # GIVEN at least two mocked valid files of any provider
        valid_iac_files = [MagicMock(filename='valid_iac_file_one', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO)),
                           MagicMock(filename='valid_iac_file_two', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))]

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # WHEN the POST /iac endpoint is called with iac params AND no error is raised
        mock_provider_processor_result(mock_otm_processor, mock_get_processor, OTM_SAMPLE)
        response = controller.iac(valid_iac_files, '', 'happy_path_id', 'happy_path_name', valid_mapping_file)

        # THEN a response with HTTP staus 201  and json media type is returned
        assert response.status_code == 201
        assert response.media_type == 'application/json'
        assert response.body is not None

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_multiple_files_on_iac_loading_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN one mocked valid file of any provider, and one invalid
        valid_iac_files = [MagicMock(filename='valid_iac_file_one', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO)),
                           MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))]

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND the mocked method throwing a LoadingIacFileError
        with pytest.raises(LoadingIacFileError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = LoadingIacFileError('mocked IAC_LOADING_ERROR', 'mocked detail', 'mocked msg 6')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(valid_iac_files, TESTING_IAC_TYPE, 'loading_iac_error_id', 'loading_iac_error_name',
                           valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the type of error in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'IAC_LOADING_ERROR'

    @patch('slp_base.slp_base.otm_processor.OtmProcessor')
    @patch('slp_base.slp_base.provider_resolver.ProviderResolver.get_processor')
    def test_api_iac_controller_multiple_files_on_file_not_valid_error(self, mock_get_processor, mock_otm_processor):
        # GIVEN one mocked valid file of any provider, and one invalid
        valid_iac_files = [MagicMock(filename='valid_iac_file_one', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO)),
                           MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))]

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND the mocked method throwing a IacFileNotValidError
        with pytest.raises(IacFileNotValidError) as error:
            # WHEN the POST /iac endpoint is called with iac params AND an error is raised
            mock_error = IacFileNotValidError('mocked IAC_NOT_VALID', 'mocked detail', 'mocked msg 7')
            mock_provider_processor_error(mock_otm_processor, mock_get_processor, mock_error)
            controller.iac(valid_iac_files, TESTING_IAC_TYPE, 'file_not_valid_error_id',
                           'file_not_valid_error_name', valid_mapping_file)

        # THEN a response HTTP Status that matches the error is returned
        # AND the type of error in the response body matched the name of the exception raised
        assert error.value.error_code.http_status == 400
        assert error.value.error_code.name == 'IAC_NOT_VALID'
