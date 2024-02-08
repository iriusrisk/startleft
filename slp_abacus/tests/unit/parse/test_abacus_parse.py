from unittest.mock import MagicMock, patch

import pytest
import yaml

from slp_abacus.slp_abacus.abacus_processor import AbacusParser
from slp_abacus.slp_abacus.load.abacus_mapping_file_loader import AbacusMapping
from slp_abacus.slp_abacus.objects.diagram_objects import Diagram, DiagramRepresentation

mapping_config = """
trustzones:
  - label: Public Cloud
    type: b61d6911-338d-46a8-9f39-8dcd24abfe91
    default: true

components:
  - label: SST PoC Integrator
    type: CD-MSG-BROKER
  - label: SST PoC Webpage
    type: compact-server-side-web-application
  - label: SST PoC Database
    type: other-database
  - label: SST PoC Static Content
    type: CD-CONTENT-DELIVERY-NETWORK
  - label: SST PoC Backend
    type: back-end-server
  - label: Angular v12.0.0
    type: web-client
  - label: SST PoC Webpage
    type: compact-server-side-web-application
"""


class TestAbacusParser:

    @pytest.fixture
    def abacus_parser_instance(self):
        project_id = 'test_project_id'
        project_name = 'Test Project'
        diagram = Diagram(DiagramRepresentation(project_id, {'width': 1000, 'height': 1000}), [], [], [])
        mapping_data = yaml.safe_load(mapping_config)
        abacus_mapping = AbacusMapping(**mapping_data)
        return AbacusParser(project_id, project_name, diagram, abacus_mapping)

    @patch('slp_abacus.slp_abacus.parse.diagram_mapper.DiagramMapper')
    @patch('slp_abacus.slp_abacus.parse.transformers.default_trustzone_transformer.DefaultTrustZoneTransformer')
    @patch('otm.otm.otm_builder.OTMBuilder')
    def test_build_otm_success(self, mock_otm_builder, mock_default_trustzone_transformer, mock_diagram_mapper,
                               abacus_parser_instance):
        expected_project_id = 'test_project_id'
        expected_project_name = 'Test Project'

        mock_otm_instance = MagicMock()
        mock_otm_builder.return_value.build.return_value = mock_otm_instance

        otm = abacus_parser_instance.build_otm()

        assert otm.project_id == expected_project_id
        assert otm.project_name == expected_project_name

        mock_diagram_mapper(abacus_parser_instance.diagram, abacus_parser_instance.mapping)
        mock_default_trustzone_transformer(abacus_parser_instance.diagram)
