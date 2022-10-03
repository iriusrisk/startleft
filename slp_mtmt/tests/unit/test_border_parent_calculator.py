from pytest import mark

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.util.border_parent_calculator import BorderParentCalculator


class TestBorderParentCalculator:

    @mark.parametrize('parent_value,child_value', [
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '150', 'Top': '140', 'Height': '40'}),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '90', 'Height': '40'}),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '80'})
    ])
    def test_outside(self, parent_value, child_value):
        # GIVEN the parent MTMT border
        parent_source = {'Value': parent_value}
        parent = MTMBorder(parent_source)

        # AND the child MTMT border
        child_source = {'Value': child_value}
        child = MTMBorder(child_source)

        # WHEN we check if parent is the child parent
        calculator = BorderParentCalculator()
        is_parent = calculator.is_parent(parent, child)

        # THEN validate
        assert not is_parent

    def test_inside(self):
        # GIVEN the parent MTMT border
        parent_source = {'Value': {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}}
        parent = MTMBorder(parent_source)

        # AND the child MTMT border
        child_source = {'Value': {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '40'}}
        child = MTMBorder(child_source)

        # WHEN we check if parent is the child parent
        calculator = BorderParentCalculator()
        is_parent = calculator.is_parent(parent, child)

        # THEN validate
        assert is_parent

    @mark.parametrize('parent_value,child_value', [
        ({'Valuee': {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Leftt': '50', 'Width': '200', 'Top': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Widthh': '200', 'Top': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200', 'Topp': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200', 'Top': '100', 'Heightt': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50a', 'Width': '200', 'Top': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200a', 'Top': '100', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200', 'Top': '100a', 'Height': '100'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100a'}},
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        (None,
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
        ({'Value': {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}},
         None),
        ("",
         {'Value': {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}}),
    ])
    def test_invalid_input_return_false(self, parent_value, child_value):
        # GIVEN the parent MTMT border
        parent = MTMBorder(parent_value)

        # AND the child MTMT border
        child = MTMBorder(child_value)

        # WHEN we check if parent is the child parent
        calculator = BorderParentCalculator()
        is_parent = calculator.is_parent(parent, child)

        # THEN validate
        assert not is_parent
