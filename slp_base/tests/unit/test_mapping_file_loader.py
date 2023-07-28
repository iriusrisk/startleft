from slp_base.slp_base.mapping_file_loader import MappingFileLoader

default = b'components:\n\n  - label: Postgres\n    type: postgresql'
custom = b'components:\n\n  - label: AmazonEC2\n    type: ec2'


class TestMappingFileLoader:

    def test_mapping_file_priority(self):
        # GIVEN the mapping loader with a default and custom mapping files
        mapping_file_loader = MappingFileLoader([default, custom])

        # WHEN load is called in MappingFileLoader
        mapping_file = mapping_file_loader.load()

        # THEN the result has two components
        assert len(mapping_file['components']) == 2
        # AND the first component is the custom
        assert mapping_file['components'][0]['label'] == 'AmazonEC2'
        assert mapping_file['components'][0]['type'] == 'ec2'
        # AND the second component is the default
        assert mapping_file['components'][1]['label'] == 'Postgres'
        assert mapping_file['components'][1]['type'] == 'postgresql'

