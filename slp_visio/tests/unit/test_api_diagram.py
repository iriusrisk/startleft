import typing
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

import startleft.api.controllers.diagram.diag_create_otm_controller as diagram_controller
from slp_visio.slp_visio.diagram_type import DiagramType
from startleft.api.errors import OtmGenerationError, LoadingDiagramFileError, DiagramFileNotValidError, \
    MappingFileNotValidError, OtmResultError
from startleft.otm.otm import OTM

TESTING_DIAGRAM_TYPE = DiagramType.VISIO
DUMMY_OTM = OTM("otm-mock", "otm mock", DiagramType.VISIO)


class TestApiDiagram:

    def test_api_diagram_controller_happy_path(self):
        # GIVEN a mocked valid file of any provider
        valid_diagram_file = MagicMock(filename='valid_diagram_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_default_mapping_file', content_type='application/json',
                                               file=MagicMock(spec=typing.BinaryIO))

        # WHEN the POST /diagram endpoint is called with diagram params AND no error is raised
        with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process', side_effect=[DUMMY_OTM]):
            response = diagram_controller.diagram(valid_diagram_file, TESTING_DIAGRAM_TYPE, 'happy_path_id',
                                                  'happy_path_name', valid_default_mapping_file, False)

        # THEN a response with HTTP status 201 is returned
        assert response.status_code == 201

    def test_api_diagram_controller_on_loading_diagram_file_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_diagram_file = MagicMock(filename='invalid_diagram_file', content_type='application/json',
                                         file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                               file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a LoadingDiagramFileError
        with pytest.raises(LoadingDiagramFileError) as e_info:
            # WHEN the POST /diagram endpoint is called with_diagram params
            # AND an error is raised
            with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process',
                       side_effect=LoadingDiagramFileError('mocked error DIAGRAM_LOADING_ERROR', 'mocked error detail',
                                                           'mocked error msg 1')):
                # THEN a response HTTP Status that matches the error is returned
                diagram_controller.diagram(invalid_diagram_file, TESTING_DIAGRAM_TYPE,
                                           'diagram_controller_on_loading_diagram_error_id',
                                           'diagram_controller_on_loading_diagram_error_name',
                                           valid_default_mapping_file, False)

        # AND the error_type in the response body matched the name of the exception raised

        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'DIAGRAM_LOADING_ERROR'

    def test_api_diagram_controller_on_diagram_file_not_valid_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_diagram_file = MagicMock(filename='invalid_diagram_file', content_type='application/json',
                                         file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                               file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a DiagramFileNotValidError
        with pytest.raises(DiagramFileNotValidError) as e_info:
            # WHEN the POST /diagram endpoint is called with_diagram params
            # AND an error is raised
            with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process',
                       side_effect=DiagramFileNotValidError('mocked error DIAGRAM_NOT_VALID', 'mocked error detail',
                                                            'mocked error msg 2')):
                # THEN a response HTTP Status that matches the error is returned
                diagram_controller.diagram(invalid_diagram_file, TESTING_DIAGRAM_TYPE,
                                           'diagram_controller_on_diagram_file_not_valid_error_id',
                                           'diagram_controller_on_diagram_file_not_valid_error_name',
                                           valid_default_mapping_file, False)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'DIAGRAM_NOT_VALID'

    def test_api_diagram_controller_on_mapping_file_not_valid_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_diagram_file = MagicMock(filename='invalid_diagram_file', content_type='application/json',
                                         file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                               file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a MappingFileNotValidError
        with pytest.raises(MappingFileNotValidError) as e_info:
            # WHEN the POST /diagram endpoint is called with_diagram params
            # AND an error is raised
            with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process',
                       side_effect=MappingFileNotValidError('mocked error MAPPING_FILE_NOT_VALID',
                                                            'mocked error detail', 'mocked error msg 3')):
                # THEN a response HTTP Status that matches the error is returned
                diagram_controller.diagram(invalid_diagram_file, TESTING_DIAGRAM_TYPE,
                                           'diagram_controller_on_on_mapping_file_not_valid_error_id',
                                           'diagram_controller_on_on_mapping_file_not_valid_error_name',
                                           valid_default_mapping_file, False)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'MAPPING_FILE_NOT_VALID'

    def test_api_diagram_controller_on_otm_result_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_diagram_file = MagicMock(filename='invalid_diagram_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a OtmResultError
        with pytest.raises(OtmResultError) as e_info:
            # WHEN the POST /diagram endpoint is called with_diagram params
            # AND an error is raised
            with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process',
                       side_effect=OtmResultError('mocked error OTM_RESULT_ERROR', 'mocked error detail',
                                                    'mocked error msg 4')):
                # THEN a response HTTP Status that matches the error is returned
                diagram_controller.diagram(invalid_diagram_file, TESTING_DIAGRAM_TYPE, 'diagram_controller_on_otm_result_error_id',
                               'diagram_controller_on_otm_result_error_name', valid_default_mapping_file, False)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'OTM_RESULT_ERROR'

    def test_api_diagram_controller_on_otm_generation_error(self):
        # GIVEN a mocked invalid file of any provider
        invalid_diagram_file = MagicMock(filename='invalid_diagram_file', content_type='application/json',
                                     file=MagicMock(spec=typing.BinaryIO))

        # AND any mocked mapping file
        valid_default_mapping_file = MagicMock(filename='valid_mapping_file', content_type='application/json',
                                       file=MagicMock(spec=typing.BinaryIO))

        # And the mocked method throwing a OtmGenerationError
        with pytest.raises(OtmGenerationError) as e_info:
            # WHEN the POST /diagram endpoint is called with_diagram params
            # AND an error is raised
            with patch('slp_visio.slp_visio.visio_processor.VisioProcessor.process',
                       side_effect=OtmGenerationError('mocked error OTM_GENERATION_ERROR', 'mocked error detail',
                                                      'mocked error msg 5')):
                # THEN a response HTTP Status that matches the error is returned
                diagram_controller.diagram(invalid_diagram_file, TESTING_DIAGRAM_TYPE, 'diagram_controller_on_otm_generation_error_id',
                               'diagram_controller_on_otm_generation_error_name', valid_default_mapping_file, False)

        # AND the error_type in the response body matched the name of the exception raised
        assert e_info.value.error_code.http_status == 500
        assert e_info.value.error_code.name == 'OTM_GENERATION_ERROR'
