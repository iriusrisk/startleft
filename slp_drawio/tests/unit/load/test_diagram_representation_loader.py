from typing import Dict
from unittest.mock import Mock

from pytest import fixture, mark, param

from otm.otm.entity.representation import RepresentationType
from slp_drawio.slp_drawio.load.diagram_representation_loader import DiagramRepresentationLoader

DEFAULT_SIZE = {'width': 1000, 'height': 1000}


@fixture(autouse=True)
def mock_get_diagram_size(mocker, mocked_size):
    mocker.patch('slp_drawio.slp_drawio.load.diagram_representation_loader.get_diagram_size', side_effect=[mocked_size])


class TestDiagramRepresentationLoader:

    @mark.usefixtures('mock_get_diagram_size')
    @mark.parametrize('mocked_size', [
        param({'width': 1234, 'height': 5678}, id='source size'),
        param(None, id='default size')
    ])
    def test_create_representation(self, mocked_size: Dict):
        # GIVEN a mock for the diagram size

        # AND a mock for the source
        source = Mock()

        # AND a project ID
        project_id = 'p-id'

        # WHEN DiagramRepresentationLoader::load is called
        representation = DiagramRepresentationLoader(project_id=project_id, source=source).load()

        # THEN a DiagramRepresentation is returned
        assert representation.otm.id == f'{project_id}-diagram'
        assert representation.otm.name == f'{project_id} Diagram Representation'
        assert representation.otm.type == RepresentationType.DIAGRAM

        # AND the size is extracted from the diagram or taken by default
        if mocked_size:
            assert representation.otm.size == mocked_size
        else:
            assert representation.otm.size == DEFAULT_SIZE
