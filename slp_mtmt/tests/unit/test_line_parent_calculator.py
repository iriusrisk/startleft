from pytest import mark

from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.util.line_parent_calculator import LineParentCalculator


def create_line(coordinates, name):
    source = {'Value': {'HandleX': f'{coordinates[0]}', 'HandleY': f'{coordinates[1]}',
                        'SourceX': f'{coordinates[2]}', 'SourceY': f'{coordinates[3]}',
                        'TargetX': f'{coordinates[4]}', 'TargetY': f'{coordinates[5]}',
                        'Properties': {'anyType': [{'DisplayName': 'Name', 'Value': {'text': f'{name}'}}]}},
              'attrib': {'type': 'LineBoundary'}
              }
    return MTMLine(source)


def create_border(coordinates):
    source = {'Value': {'Left': f'{coordinates[0]}', 'Width': f'{coordinates[1]}',
                        'Top': f'{coordinates[2]}', 'Height': f'{coordinates[3]}'}}
    return MTMLine(source)


calculator = LineParentCalculator()


class TestLineParentCalculator:

    @mark.parametrize('name,orientation,parent_value,child_value', [
        ('At Left', 'l', [200, 210, 140, 300, 140, 100], [50, 80, 220, 81]),
        ('At Left Inverted', 'l', [200, 210, 140, 100, 140, 300], [50, 80, 220, 81]),
        ('At Right', 'r', [200, 210, 300, 310, 315, 100], [320, 80, 220, 81]),
        ('At Right Inverted', 'r', [200, 210, 300, 100, 315, 310], [320, 80, 220, 81]),
        ('At Top', 't', [200, 400, 140, 300, 308, 312], [205, 80, 150, 81]),
        ('At Top Inverted', 't', [200, 400, 308, 300, 140, 312], [205, 80, 150, 81]),
        ('At Bottom', 'b', [200, 150, 105, 250, 308, 260], [207, 80, 500, 81]),
        ('At Bottom Inverted', 'b', [200, 150, 308, 250, 105, 260], [207, 80, 500, 81]),
        ('At Left Turned', 'l', [200, 210, 140, 300, 190, 100], [50, 80, 220, 81]),
    ])
    def test_inside(self, name, orientation, parent_value, child_value):
        # GIVEN the parent MTMT line
        parent = create_line(parent_value, name)

        # AND the child MTMT border
        child = create_border(child_value)

        # WHEN we check if parent is the child parent
        is_parent = calculator.is_parent(parent, child)

        # THEN validate
        assert is_parent

    @mark.parametrize('name,parent_value,child_value', [
        ('Left', [200, 210, 140, 300, 140, 100], [290, 80, 220, 81]),
        ('Left Inverted', [200, 210, 140, 100, 140, 300], [290, 80, 220, 81]),
        ('Right', [200, 210, 300, 310, 315, 100], [110, 80, 220, 81]),
        ('Right Inverted', [200, 210, 300, 100, 315, 310], [110, 80, 220, 81]),
        ('Top', [200, 400, 140, 300, 308, 312], [205, 80, 490, 81]),
        ('Top Inverted', [200, 400, 308, 300, 140, 312], [205, 80, 490, 81]),
        ('Bottom', [200, 150, 105, 250, 308, 260], [207, 80, 60, 81]),
        ('Bottom Inverted', [200, 150, 308, 250, 105, 260], [207, 80, 60, 81]),
        ('Vertical', [200, 150, 200, 100, 200, 260], [207, 80, 60, 81]),
        ('Horizontal', [195, 150, 300, 150, 410, 150], [207, 80, 60, 81]),
        ('Diagonal', [200, 200, 100, 100, 300, 300], [207, 80, 60, 81]),
    ])
    def test_outside(self, name, parent_value, child_value):
        # GIVEN the parent MTMT line
        parent = create_line(parent_value, name)

        # AND the child MTMT border
        child = create_border(child_value)

        # WHEN we check if parent is the child parent
        is_parent = calculator.is_parent(parent, child)

        # THEN validate
        assert not is_parent
