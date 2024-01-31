"""
The order of the mapping files is important.
The last mapping file received (the custom one) should override the previous one (the default one)
and needs to be the first.
So this class sorts the mapping files in reverse order.
"""


class MappingFileSorter:

    def __init__(self, mapping_files: [bytes]):
        self.mapping_files = mapping_files

    def sort(self) -> [bytes]:
        return self.mapping_files[::-1]
