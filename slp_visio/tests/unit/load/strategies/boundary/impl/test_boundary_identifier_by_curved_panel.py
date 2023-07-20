from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.boundary.impl.boundary_identifier_by_curved_panel import BoundaryIdentifierByCurvedPanel


class TestBoundaryIdentifierByCurvedPanel:

    @pytest.mark.parametrize('shape_name', {
        'Curved panel',
        'Curved panel.12',
        '- Curved panel -'
    })
    def test_validate_boundary_ok(self, shape_name):
        # GIVEN a visio boundary shape
        shape = MagicMock(ID=1001, text='Internet', shape_name=shape_name)
        # WHEN the boundary is validated
        strategy = BoundaryIdentifierByCurvedPanel()
        result = strategy.is_boundary(shape)

        # THEN is a valid boundary
        assert result

    @pytest.mark.parametrize('shape_name', {
        ' ',
        '   ',
        'curved panel',
        'Curvedpanel',
        'Panel Curved'

    })
    def test_validate_with_connects_wrong_boundary_shape_name(self, shape_name):
        # GIVEN a visio boundary shape
        shape = MagicMock(ID=1001, text='Internet', shape_name=shape_name)

        # WHEN the boundary is validated
        strategy = BoundaryIdentifierByCurvedPanel()
        result = strategy.is_boundary(shape)

        # THEN is not a valid boundary
        assert not result
