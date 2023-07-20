from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_master_page_name \
    import ComponentIdentifierByMasterPageName


class TestComponentIdentifierByMasterPageName:

    @pytest.mark.parametrize('shape_text', {
        'My EC2',
        'EC2',
        None
    })
    def test_validate_without_master_page(self, shape_text):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text=shape_text)
        shape.master_page = None
        # WHEN the component is validated
        strategy = ComponentIdentifierByMasterPageName()
        result = strategy.is_component(shape)

        # THEN is not a valid component
        assert not result

    @pytest.mark.parametrize('page_name,', {
        pytest.param('', id='Void name'),
        pytest.param('   ', id='Blank name'),
        pytest.param(None, id='None name')
    })
    def test_validate_without_master_page_name(self, page_name):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text='My EC2')
        shape.master_page.name = page_name

        # WHEN the component is validated
        strategy = ComponentIdentifierByMasterPageName()
        result = strategy.is_component(shape)

        # THEN is not a valid component
        assert not result

    @pytest.mark.parametrize('page_name', {
        'AWS Step Function',
        'aws',
        '                 aws',
        'aws                 ',

    })
    def test_validate_with_master_page_name(self, page_name):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, shape_name=None)
        shape.text = None
        shape.master_page.name = page_name
        # WHEN the component is validated
        strategy = ComponentIdentifierByMasterPageName()
        result = strategy.is_component(shape)

        # THEN is a valid component
        assert result
