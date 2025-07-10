from unittest.mock import patch, Mock

from pytest import raises

from sl_util.sl_util.file_utils import get_as_dict
from slp_base import LoadingDiagramFileError
from slp_drawio.slp_drawio.load.drawio_loader import DrawioLoader
from slp_drawio.tests.resources.test_resource_paths import aws_multiple_pages_drawio_as_json


class TestDrawioLoader:

    @patch('slp_drawio.slp_drawio.load.drawio_loader.DrawIOToDict.to_dict')
    @patch('slp_drawio.slp_drawio.load.drawio_loader.is_multiple_pages', return_value=False)
    @patch('slp_drawio.slp_drawio.load.drawio_loader.DiagramRepresentationLoader.load')
    @patch('slp_drawio.slp_drawio.load.drawio_loader.DiagramComponentLoader.load')
    @patch('slp_drawio.slp_drawio.load.drawio_loader.DiagramDataflowLoader.load')
    def test_load_ok(self, to_dict_mock, mult_pages_mock, load_repr_mock, load_components_mock, load_dataflows_mock):
        # GIVEN a single page diagram

        # WHEN the DrawioLoader::load is invoked
        loader = DrawioLoader(project_id='drawio-project', source=Mock())
        loader.load()

        # THEN the source is processed
        to_dict_mock.assert_called_once()

        # AND the representations are loaded
        load_repr_mock.assert_called_once()

        # AND the components are loaded
        load_components_mock.assert_called_once()

        # AND the dataflows are loaded
        load_dataflows_mock.assert_called_once()

        # AND a Diagram is created
        assert loader.get_diagram()

    @patch('slp_drawio.slp_drawio.load.drawio_loader.DrawIOToDict.to_dict')
    def test_multiple_pages_drawio(self, to_dict_mock):
        # GIVEN a DrawIO with multiple pages
        to_dict_mock.return_value = get_as_dict(aws_multiple_pages_drawio_as_json)

        # WHEN DiagramComponentLoader::load is invoked
        # THEN a LoadingDiagramFileError is raised
        with raises(LoadingDiagramFileError) as error:
            DrawioLoader(project_id='drawio-project', source=Mock()).load()

        # AND the error has the following messages
        assert str(error.value.title) == 'Diagram file is not valid'
        assert str(error.value.detail) == 'DrawIO processor does not accept diagrams with multiple pages'
        assert str(error.value.message) == 'Diagram File is not compatible'

    @patch('slp_drawio.slp_drawio.load.drawio_loader.DrawIOToDict')
    def test_uncontrolled_exception(self, map_mock):
        # GIVEN a loader with mocked arguments
        # AND a forced uncontrolled exception
        message= 'Error message'
        map_mock.side_effect = Exception(message)

        # WHEN DiagramComponentLoader::load is invoked
        with raises(LoadingDiagramFileError) as error:
            DrawioLoader(project_id='drawio-project', source=Mock()).load()

        # THEN the exception is encapsulated in an LoadingDiagramFileError
        assert error.value.title == 'Source file cannot be loaded'
        assert error.value.message == 'Error message'
        assert error.value.detail == 'Exception'
