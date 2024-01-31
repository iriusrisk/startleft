from slp_base.slp_base.mapping_file_sorter import MappingFileSorter


class TestMappingFileSorter:

    def test_mapping_file_sort(self):
        # GIVEN two byte data
        first = b'the first one'
        second = b'the second one'

        # AND the mapping sorter with the two byte data
        sorter = MappingFileSorter([first, second])

        # WHEN sort is called in MappingFileSorter
        sorted_list = sorter.sort()

        # THEN the result is reversed
        assert sorted_list[0] == second
        assert sorted_list[1] == first
