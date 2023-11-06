from unittest.mock import MagicMock

import pytest

from slp_base import DiagramType
from slp_visio import VisioProcessor
from slp_visio.slp_visio.parse.lucid_parser import LucidParser
from slp_visio.slp_visio.parse.visio_parser import VisioParser


class TestVisioProcessor:

    @pytest.mark.parametrize('diag_type, expected_provider_parser', [
        pytest.param(DiagramType.VISIO, VisioParser, id='with VISIO type'),
        pytest.param(DiagramType.LUCID, LucidParser, id='with LUCID type'),
    ])
    def test_get_provider_parser(self, diag_type, expected_provider_parser):
        # GIVEN the visio processor initiated with the configured diag_type
        processor = VisioProcessor(*(MagicMock(),) * 4, diag_type=diag_type)
        processor.loader = MagicMock()
        processor.mapping_loader = MagicMock()

        # WHEN getting the provider parser
        provider_parser = processor.get_provider_parser()

        # THEN the provider parser is as expected
        assert isinstance(provider_parser, expected_provider_parser)
