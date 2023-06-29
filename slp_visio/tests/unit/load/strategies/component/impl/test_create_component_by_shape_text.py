from unittest.mock import MagicMock

import pytest
from _pytest.mark import param

from slp_visio.slp_visio.load.representation.simple_component_representer import SimpleComponentRepresenter
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_shape_text import CreateComponentByShapeText


class TestCreateComponentByShapeText:

    @pytest.mark.parametrize('shape_text,master_shape_text', {
        ('My EC2', 'EC2'),
        ('Another EC2', 'EC2'),
        ('EC2', 'EC2'),
        (None, 'EC2')
    })
    def test_create_component_ok(self, shape_text, master_shape_text):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text=shape_text, shape_name=None, master_shape=MagicMock(text=master_shape_text),
                          master_page=MagicMock(master_unique_id='777'), center_x_y=(0.5, 2.5),
                          cells={'Width': MagicMock(value=8), 'Height': MagicMock(value=12)})

        # WHEN the component is created
        strategy = CreateComponentByShapeText()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN the returned diagram component has the following properties
        assert diagram_component.id == 1001
        assert diagram_component.name == shape_text or master_shape_text
        assert diagram_component.type == 'EC2'
        assert diagram_component.unique_id == '777'

    @pytest.mark.parametrize('shape_text,master_shape_text', {
        (None, None)
    })
    def test_create_component_without_text(self, shape_text, master_shape_text):
        # GIVEN a visio component shape
        shape = MagicMock(ID=1001, text=shape_text, shape_name=None, master_shape=MagicMock(text=master_shape_text),
                          master_page=MagicMock(master_unique_id='777'), center_x_y=(0.5, 2.5),
                          cells={'Width': MagicMock(value=8), 'Height': MagicMock(value=12)})

        # WHEN the component is created
        strategy = CreateComponentByShapeText()
        diagram_component = strategy.create_component(shape, representer=SimpleComponentRepresenter())

        # THEN no diagram is returned
        assert not diagram_component

    @pytest.mark.parametrize('id_,shape_name,expected', {
        param('121', 'com.lucidchart.AmazonElasticContainerServiceAWS19.121', 'AmazonElasticContainerServiceAWS19',
              id='id==tail'),
        param('10', 'com.lucidchart.AmazonElasticContainerServiceAWS19', 'AmazonElasticContainerServiceAWS19',
              id='no tail'),
        param('10', 'com.lucidchart.AmazonElasticContainerServiceAWS19.121', 'AmazonElasticContainerServiceAWS19',
              id='id!=tail'),
        param('10', 'com.lucidchart.AmazonElasticContainerServiceAWS19.121.44', 'AmazonElasticContainerServiceAWS19',
              id='double tail'),
        param('10', 'AmazonElasticContainerServiceAWS19.121', 'AmazonElasticContainerServiceAWS19', id='no head'),
        param('10', 'AmazonElasticContainerServiceAWS19', 'AmazonElasticContainerServiceAWS19', id='no dot')
    })
    def test_get_lucid_component_type(self, id_, shape_name, expected):
        # GIVEN a visio component shape
        shape = MagicMock(ID=id_, shape_name=shape_name)

        # WHEN the component is created
        strategy = CreateComponentByShapeText()
        component_type = strategy.get_lucid_component_type(shape)

        # THEN no diagram is returned
        assert component_type == expected
