from unittest.mock import patch

import pytest

from slp_abacus.slp_abacus.load.abacus_loader import AbacusLoader
from slp_base import LoadingDiagramFileError

# Assuming your test data is stored in a variable named 'test_data'
test_data = {
    "OutConnections": [
        {"EEID": 1, "SinkComponentName": "Component1", "ConnectionTypeName": "Type1"},
        {"EEID": 2, "SinkComponentName": "Component2", "ConnectionTypeName": "Type2"},
    ]
}


class TestAbacusLoader:

    @pytest.fixture
    def abacus_loader_instance(self):
        return AbacusLoader(project_id='test_project', abacus_source='abacus_merged', mapping_files=[])

    @patch('sl_util.sl_util.file_utils.read_byte_data')
    def test_load_failure(self, mock_read_byte_data, abacus_loader_instance):
        mock_read_byte_data.side_effect = Exception('Test Exception')

        with pytest.raises(LoadingDiagramFileError):
            abacus_loader_instance.load()
