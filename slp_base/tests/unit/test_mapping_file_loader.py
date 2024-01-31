from slp_base.slp_base.mapping_file_loader import MappingFileLoader

default = b'components:\n\n  - label: Postgres\n    type: postgresql'
custom = b'components:\n\n  - label: AmazonEC2\n    type: ec2'

default_configuration = b'configuration:\n\n  value_a: default_value\n\n  value_b: default_value'
custom_configuration = b'configuration:\n\n  value_a: custom_value'


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

    def test_override_configuration(self):
        # GIVEN the mapping loader with a default and custom mapping files configurations
        mapping_file_loader = MappingFileLoader([default_configuration, custom_configuration])

        # WHEN load is called in MappingFileLoader
        mapping_file = mapping_file_loader.load()

        # THEN configuration with value_a is override by the custom file
        assert mapping_file['configuration']['value_a'] == 'custom_value'
        # AND configuration with value_b exists
        assert 'value_b' in mapping_file['configuration']
        # AND configuration with value_b gets its value from default
        assert mapping_file['configuration']['value_b'] == 'default_value'
