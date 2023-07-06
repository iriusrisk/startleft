from unittest.mock import Mock

from pytest import param
from pytest import mark

from slp_visio.slp_visio.parse.shape_position_calculator import ShapePositionCalculator


class TestShapePositionCalculator:

    @mark.parametrize('x,y', [
        (0, 0),
        (0.5, 0.9),
        (0.9, 0.5),
        (0.9, 0.5),
    ])
    def test_get_absolute_center_no_parent(self, x, y):
        shape = Mock(ID=1111, x=x, y=y, center_x_y=(x, y))
        shape.parent = None
        calculator = ShapePositionCalculator(shape)
        assert calculator.get_absolute_center() == (x, y)

    @mark.parametrize('shape,parents,expected', [
        param((0.6, 0.9), [(3.2, 4.7)], (2.5, 1.4), id='child_in_1_parent'),
        param((0.6, 0.9), [(3.2, 4.7), (0.8, 10.4)], (2, 7.6), id='child_in_2_parents'),
        param((0.6, 0.9), [(3.2, 4.7), (0.8, 10.4), (11.4, 1.2)], (12.1, 4.6), id='child_in_3_parents'),
        param((2.5, 8.3), [(3.2, 4.7)], (4.4, 8.8), id='child_limit_parent'),
        param((2.6, 8.5), [(3.2, 4.7)], (4.5, 9), id='child_out_parent')
    ])
    def test_get_absolute_center_with_parent(self, shape, parents, expected):
        x, y = shape
        shape = Mock(ID=1111, x=x, y=y, center_x_y=(x, y))
        current = shape
        for idx, parent_x_y in enumerate(parents):
            parent_x, parent_y = parent_x_y
            parent = Mock(ID=current.ID + idx, x=parent_x, y=parent_y, center_x_y=(parent_x, parent_y))
            parent.width = 2.6
            parent.height = 8.4
            parent.parent = None
            current.parent = parent
            current = current.parent
        calculator = ShapePositionCalculator(shape)
        assert calculator.get_absolute_center() == expected

    @mark.parametrize('parents', [
        12,13,14,15,16,100
    ])
    def test_get_absolute_center_too_many_parent(self, parents):
        x, y = 1, 1
        shape = Mock(ID=1111, x=x, y=y, center_x_y=(x, y))
        current = shape
        for idx in range(parents):
            parent = Mock(ID=current.ID + idx, x=x, y=y, center_x_y=(2, 2))
            parent.width = 2
            parent.height = 2
            parent.parent = None
            current.parent = parent
            current = current.parent
        calculator = ShapePositionCalculator(shape)
        assert calculator.get_absolute_center() == (13, 13)