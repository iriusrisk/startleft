from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.representation.simple_component_representer import SimpleComponentRepresenter
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_master_page_name \
    import CreateComponentByMasterPageName


class TestCreateComponentByMasterShapeName:

    def test_create_component_without_master_page(self):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text='My EC2', shape_name=None)
        shape.master_page = None

        # WHEN the component is created
        strategy = CreateComponentByMasterPageName()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN is not a valid component
        assert not diagram_component

    @pytest.mark.parametrize('page_name,', {
        pytest.param('', id='Void name'),
        pytest.param('   ', id='Blank name'),
        pytest.param(None, id='None name')
    })
    def test_validate_without_master_page_name(self, page_name):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text='My EC2', shape_name=None)
        shape.master_page.name = page_name

        # WHEN the component is created
        strategy = CreateComponentByMasterPageName()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN is not a valid component
        assert not diagram_component

    @pytest.mark.parametrize('page_name', {
        'AWS Step Function',
        'aws',
        '                 aws',
        'aws                 ',

    })
    def test_validate_with_master_page_name(self, page_name):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text='My EC2', shape_name=None, master_page=MagicMock(master_unique_id='777'),
                          center_x_y=(0.5, 2.5), cells={'Width': MagicMock(value=8), 'Height': MagicMock(value=12)})
        shape.master_page.name = page_name

        # WHEN the component is created
        strategy = CreateComponentByMasterPageName()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN is not a valid component
        assert diagram_component.id == 1001
        assert diagram_component.name == page_name.strip()
