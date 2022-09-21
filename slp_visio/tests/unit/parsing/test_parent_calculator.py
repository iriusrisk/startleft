from unittest.mock import patch

from shapely.geometry import Polygon, Point

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.load.parent_calculator import ParentCalculator


def create_representation_mock(dimension: float = None) -> Polygon:
    return Point(1, 1).buffer(dimension or 10, 0)


class TestParentCalculator:

    def test_no_parent_candidates(self):
        # GIVEN a child candidate
        child_candidate = DiagramComponent(id='CC', name='Child Candidate')

        # AND no parent candidates
        parent_candidates = []

        # WHEN calling calculate_parent
        parent = ParentCalculator(child_candidate).calculate_parent(parent_candidates)

        # THEN no parent is returned
        assert not parent

    @patch('shapely.geometry.Polygon.contains')
    def test_one_candidate_does_not_contains_the_component(self, mock_representation_contains):
        # GIVEN a child candidate
        child_candidate = DiagramComponent(id='CC', name='Child Candidate', representation=create_representation_mock())

        # AND a mock for the representation contains function that returns always false
        mock_representation_contains.side_effect = [False]

        # AND a parent candidate
        parent_candidate = DiagramComponent(id='PC', name='Parent Candidate', representation=create_representation_mock())
        parent_candidates = [parent_candidate]

        # WHEN calling calculate_parent
        parent = ParentCalculator(child_candidate).calculate_parent(parent_candidates)

        # THEN no parent is returned
        assert not parent

    @patch('shapely.geometry.Polygon.contains')
    def test_one_candidate_contains_the_component(self, mock_representation_contains):
        # GIVEN a child candidate
        child_candidate = DiagramComponent(id='CC', name='Child Candidate', representation=create_representation_mock())

        # AND a mock for the representation contains function that returns always true
        mock_representation_contains.side_effect = [True]

        # AND a parent candidate
        parent_candidate = DiagramComponent(id='PC', name='Parent Candidate', representation=create_representation_mock())
        parent_candidates = [parent_candidate]

        # WHEN calling calculate_parent
        parent = ParentCalculator(child_candidate).calculate_parent(parent_candidates)

        # THEN the parent candidate is returned
        assert parent == parent_candidate

    @patch('shapely.geometry.Polygon.contains')
    def test_multiple_candidates_contain_the_component(self, mock_representation_contains):
        # GIVEN a child candidate
        child_candidate = DiagramComponent(id='CC', name='Child Candidate', representation=create_representation_mock())

        # AND a mock for the representation contains function that returns always true
        mock_representation_contains.side_effect = [True, True]

        # AND two different parent candidates with different areas
        parent_candidate_larger_area = DiagramComponent(
            id='PCGA', name='Parent Candidate (larger area)', representation=create_representation_mock(10))
        parent_candidate_smaller_area = DiagramComponent(
            id='PCSA', name='Parent Candidate (smaller area)', representation=create_representation_mock(5))

        parent_candidates = [parent_candidate_larger_area, parent_candidate_smaller_area]

        # WHEN calling calculate_parent
        parent = ParentCalculator(child_candidate).calculate_parent(parent_candidates)

        # THEN the parent candidate with smaller area is returned
        assert parent == parent_candidate_smaller_area
