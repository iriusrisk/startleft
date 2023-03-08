from pytest import mark

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.parse.mtmt_general_parser import is_parent, which_is_child, get_the_child
from slp_mtmt.tests.unit.test_line_parent_calculator import create_line, create_border


class TestMTMTGeneralParser:

    @mark.parametrize('elements_value, expected', [
        (
                ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
                 {'Left': '60', 'Width': '178', 'Top': '110', 'Height': '80'},
                 {'Left': '70', 'Width': '140', 'Top': '120', 'Height': '60'}),
                2),
        (
                ({'Left': '70', 'Width': '140', 'Top': '120', 'Height': '60'},
                 {'Left': '60', 'Width': '178', 'Top': '110', 'Height': '80'},
                 {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}),
                0),
        (
                ({'Left': '60', 'Width': '178', 'Top': '110', 'Height': '80'},
                 {'Left': '70', 'Width': '140', 'Top': '120', 'Height': '60'},
                 {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}),
                1)

    ])
    def test_get_the_child(self, elements_value, expected):
        # GIVEN the elements
        elements = []
        for value in elements_value:
            source = {'Value': value}
            elements.append(MTMBorder(source))

        # THEN we check if is_parent return the expected value
        assert get_the_child(elements) == elements[expected]

    @mark.parametrize('parent_values, child_values, expected', [
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}, False),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '150', 'Top': '140', 'Height': '40'}, False),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '90', 'Height': '40'}, False),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '80'}, False),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}, False),
        ({'Left': '150', 'Width': '500', 'Top': '10', 'Height': '320'},
         {'Left': '150', 'Width': '500', 'Top': '10', 'Height': '320'}, False),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '40'}, True)
    ])
    def test_border_is_parent(self, parent_values, child_values, expected):
        # GIVEN the parent
        parent_source = {'Value': parent_values}
        parent = MTMBorder(parent_source)
        # AND the child
        child_source = {'Value': child_values}
        child = MTMBorder(child_source)

        # THEN we check if is_parent return the expected value
        assert is_parent(parent, child) == expected

    @mark.parametrize('name,parent_value,child_value,expected', [
        ('At Left', [200, 210, 140, 300, 140, 100], [50, 80, 220, 81], True),
        ('At Left Inverted', [200, 210, 140, 100, 140, 300], [50, 80, 220, 81], True),
        ('At Right', [200, 210, 300, 310, 315, 100], [320, 80, 220, 81], True),
        ('At Right Inverted', [200, 210, 300, 100, 315, 310], [320, 80, 220, 81], True),
        ('At Top', [200, 400, 140, 300, 308, 312], [205, 80, 150, 81], True),
        ('At Top Inverted', [200, 400, 308, 300, 140, 312], [205, 80, 150, 81], True),
        ('At Bottom', [200, 150, 105, 250, 308, 260], [207, 80, 500, 81], True),
        ('At Bottom Inverted', [200, 150, 308, 250, 105, 260], [207, 80, 500, 81], True),
        ('At Left Turned', [200, 210, 140, 300, 190, 100], [50, 80, 220, 81], True),
        ('Left', [200, 210, 140, 300, 140, 100], [290, 80, 220, 81], False),
        ('Left Inverted', [200, 210, 140, 100, 140, 300], [290, 80, 220, 81], False),
        ('Right', [200, 210, 300, 310, 315, 100], [110, 80, 220, 81], False),
        ('Right Inverted', [200, 210, 300, 100, 315, 310], [110, 80, 220, 81], False),
        ('Top', [200, 400, 140, 300, 308, 312], [205, 80, 490, 81], False),
        ('Top Inverted', [200, 400, 308, 300, 140, 312], [205, 80, 490, 81], False),
        ('Bottom', [200, 150, 105, 250, 308, 260], [207, 80, 60, 81], False),
        ('Bottom Inverted', [200, 150, 308, 250, 105, 260], [207, 80, 60, 81], False),
        ('Vertical', [200, 150, 200, 100, 200, 260], [207, 80, 60, 81], False),
        ('Horizontal', [195, 150, 300, 150, 410, 150], [207, 80, 60, 81], False),
        ('Diagonal', [200, 200, 100, 100, 300, 300], [207, 80, 60, 81], False),
    ])
    def test_line_is_parent(self, name, parent_value, child_value, expected):
        # GIVEN the parent MTMT line
        parent = create_line(parent_value, name)

        # THEN we check if is_parent return the expected value
        child = create_border(child_value)

        # WHEN we check if parent is the child parent
        assert is_parent(parent, child) == expected

    @mark.parametrize('parent_values, child_values, expected', [
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '40', 'Width': '40', 'Top': '140', 'Height': '40'}, 2),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '150', 'Top': '140', 'Height': '40'}, 2),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '90', 'Height': '40'}, 2),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '80'}, 2),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}, 2),
        ({'Left': '150', 'Width': '500', 'Top': '10', 'Height': '320'},
         {'Left': '150', 'Width': '500', 'Top': '10', 'Height': '320'}, 2),
        ({'Left': '110', 'Width': '40', 'Top': '140', 'Height': '40'},
         {'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'}, 0),
        ({'Left': '50', 'Width': '200', 'Top': '100', 'Height': '100'},
         {'Left': '110', 'Width': '40', 'Top': '140', 'Height': '40'}, 1)
    ])
    def test_which_is_child(self, parent_values, child_values, expected):
        # GIVEN the parent
        parent_source = {'Value': parent_values}
        parent = MTMBorder(parent_source)
        # AND the child
        child_source = {'Value': child_values}
        child = MTMBorder(child_source)
        # AND the candidates
        candidates = [parent, child, None]

        # THEN we check if is_parent return the expected value
        assert which_is_child(parent, child) == candidates[expected]
