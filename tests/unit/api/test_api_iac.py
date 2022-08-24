import typing
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

import startleft.api.controllers.iac.iac_create_otm_controller as controller
from startleft.api.errors import LoadingIacFileError, IacFileNotValidError, LoadingMappingFileError, \
    OtmBuildingError, OtmGenerationError
from startleft.otm.otm_builder import OtmBuilder
from startleft.processors.base.provider_type import IacType

PROJECT_ID = 'id'
PROJECT_NAME = 'name'
TESTING_IAC_TYPE = IacType.CLOUDFORMATION
OTM_SAMPLE = OtmBuilder(PROJECT_ID, PROJECT_NAME, TESTING_IAC_TYPE).build()


class TestApiIac:

    def test_api_iac_controller_happy_path(self):
        # GIVEN a mocked valid file of any provider
        valid_iac_file = MagicMock(filename='valid_iac_file', content_type='application/json',
                                   file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # WHEN the POST /iac endpoint is called with iac params AND no error is raised
        with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                   side_effect=[OTM_SAMPLE]):
            response = controller.iac(
                valid_iac_file, TESTING_IAC_TYPE, 'happy_path_id', 'happy_path_name', valid_mapping_file)

        # THEN a response with HTTP status 201 is returned
        assert response.status_code == 201

    def test_api_iac_controller_on_loading_iac_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a LoadingIacFileError
        with pytest.raises(LoadingIacFileError) as e_info:
            # WHEN the POST /iac endpoint is called with iac params
            # AND an error is raised
            with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                       side_effect=LoadingIacFileError('mocked error IAC_LOADING_ERROR', 'mocked error detail',
                                                       'mocked error msg 1')):
                # THEN a response HTTP Status that matches the error is returned
                controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_loading_iac_error_id',
                               'iac_controller_on_loading_iac_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised

        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'IAC_LOADING_ERROR'

    def test_api_iac_controller_on_iac_file_not_valid_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a IacFileNotValidError
        with pytest.raises(IacFileNotValidError) as e_info:
            # WHEN the POST /iac endpoint is called with iac params
            # AND an error is raised
            with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                       side_effect=IacFileNotValidError('mocked error IAC_NOT_VALID', 'mocked error detail',
                                                        'mocked error msg 2')):
                # THEN a response HTTP Status that matches the error is returned
                controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_iac_file_not_valid_error_id',
                               'iac_controller_on_iac_file_not_valid_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'IAC_NOT_VALID'

    def test_api_iac_controller_on_loading_mapping_file_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a LoadingMappingFileError
        with pytest.raises(LoadingMappingFileError) as e_info:
            # WHEN the POST /iac endpoint is called with iac params
            # AND an error is raised
            with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                       side_effect=LoadingMappingFileError('mocked error MAPPING_LOADING_ERROR', 'mocked error detail',
                                                           'mocked error msg 3')):
                # THEN a response HTTP Status that matches the error is returned
                controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_loading_mapping_file_error_id',
                               'iac_controller_on_loading_mapping_file_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'MAPPING_LOADING_ERROR'

    def test_api_iac_controller_on_otm_building_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a OtmBuildingError
        with pytest.raises(OtmBuildingError) as e_info:
            # WHEN the POST /iac endpoint is called with iac params
            # AND an error is raised
            with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                       side_effect=OtmBuildingError('mocked error OTM_BUILDING_ERROR', 'mocked error detail',
                                                    'mocked error msg 4')):
                # THEN a response HTTP Status that matches the error is returned
                controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_otm_building_error_id',
                               'iac_controller_on_otm_building_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'OTM_BUILDING_ERROR'

    def test_api_iac_controller_on_otm_generation_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_iac_file = MagicMock(filename='invalid_iac_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a OtmGenerationError
        with pytest.raises(OtmGenerationError) as e_info:
            # WHEN the POST /iac endpoint is called with iac params
            # AND an error is raised
            with patch('startleft.processors.base.otm_processor.OtmProcessor.process',
                       side_effect=OtmGenerationError('mocked error OTM_GENERATION_ERROR', 'mocked error detail',
                                                      'mocked error msg 5')):
                # THEN a response HTTP Status that matches the error is returned
                controller.iac(invalid_iac_file, TESTING_IAC_TYPE, 'iac_controller_on_otm_generation_error_id',
                               'iac_controller_on_otm_generation_error_name', valid_mapping_file)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 500
        assert e_info.value.error_code.name == 'OTM_GENERATION_ERROR'
