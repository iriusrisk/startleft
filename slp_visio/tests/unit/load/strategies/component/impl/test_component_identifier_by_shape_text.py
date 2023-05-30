from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_shape_text import \
    ComponentIdentifierByShapeText


class TestComponentIdentifierByShapeText:

    @pytest.mark.parametrize('shape_text', {
        'My EC2',
        'EC2'
    })
    def test_validate_component_ok(self, shape_text):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text=shape_text, shape_name=None)
        # WHEN the component is validated
        strategy = ComponentIdentifierByShapeText()
        result = strategy.is_component(shape)

        # THEN is a valid component
        assert result

    @pytest.mark.parametrize('shape_text', {
        ' ',
        '   '
    })
    def test_validate_with_connects_wrong_component_shape_name(self, shape_text):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text=shape_text, shape_name=None)

        # WHEN the component is validated
        strategy = ComponentIdentifierByShapeText()
        result = strategy.is_component(shape)

        # THEN is not a valid component
        assert not result
