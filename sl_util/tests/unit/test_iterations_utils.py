from sl_util.sl_util.iterations_utils import remove_from_list


def remove_function(element, original_array, removed_array):
    original_array.remove(element)
    removed_array.append(element)


class TestIterationUtils:

    def test_with_none_colection(self):
        # Given a None list
        # when passed to function
        remove_from_list(
            None,
            lambda number: number % 2 == 0)
        # everything works correctly
        assert True

    def test_with_empty_colection(self):
        # Given an empty list
        # when passed to function
        remove_from_list(
            [],
            lambda number: number % 2 == 0)
        # everything works correctly
        assert True

    def test_basic_remove_elements(self):
        # Given a list of integers {1-4}
        original_array = [1, 2, 3, 4]

        # When removing even numbers
        remove_from_list(
            original_array,
            lambda number: number % 2 == 0
        )

        # Then the original value array is modified removing even numbers
        assert len(original_array) is 2
        assert 1 in original_array
        assert 3 in original_array

    def test_basic_remove_with_custom_remove_function(self):
        # Given a list of integers {1-4}
        original_array = [1, 2, 3, 4]

        # And an empty list for storing removed elements
        removed_array = []

        # When removing even numbers
        remove_from_list(
            original_array,
            lambda number: number % 2 == 0,
            lambda number: remove_function(number, original_array, removed_array)
        )

        # Then the original value array is modified removing even numbers
        assert len(original_array) is 2
        assert 1 in original_array
        assert 3 in original_array
        # and removed array has all the odd numbers
        assert len(removed_array) is 2
        assert 2 in removed_array
        assert 4 in removed_array
