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
        shape.child_shapes = None

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
        shape.child_shapes = None

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
        shape.child_shapes = None

        # WHEN the component is created
        strategy = CreateComponentByMasterPageName()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN is a valid component
        assert diagram_component.id == 1001
        assert diagram_component.name == page_name.strip()

    @pytest.mark.parametrize('text1,text2,text3,expected', {
        pytest.param('Lambda1', None, None, 'Lambda1', id='In first child'),
        pytest.param(None, 'Lambda1', '', 'Lambda1', id='In second child'),
        pytest.param(None, '', 'Lambda1', 'Lambda1', id='In last child'),
        pytest.param('AWS ', 'Lambda', '', 'AWS Lambda', id='In two'),
        pytest.param('AWS ', 'Lambda ', 'Step functions', 'AWS Lambda Step functions', id='In all'),
        pytest.param(None, None, None, 'AmazonAPIGateway', id='In all'),
    })
    def test_validate_with_child_shapes(self, text1, text2, text3, expected):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, shape_name='com.lucidchart.AmazonAPIGatewayAWS2021',
                          master_page=MagicMock(master_unique_id='777'),
                          center_x_y=(0.5, 2.5), cells={'Width': MagicMock(value=8), 'Height': MagicMock(value=12)})
        shape.master_page = MagicMock(name='com.lucidchart.AmazonAPIGatewayAWS2021250.abcde', master_unique_id='989')
        shape.child_shapes = [MagicMock(ID=1101), MagicMock(ID=1102), MagicMock(ID=1103)]
        shape.child_shapes[0].text = text1
        shape.child_shapes[1].text = text2
        shape.child_shapes[2].text = text3

        # WHEN the component is created
        strategy = CreateComponentByMasterPageName()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN is a valid component
        assert diagram_component.id == 1001
        assert diagram_component.name == expected
