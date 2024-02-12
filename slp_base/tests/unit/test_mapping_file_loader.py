from pytest import mark, param

from slp_base.slp_base.mapping_file_loader import MappingFileLoader

default = (b'components:\n\n  - label: Postgres\n    type: psql-default\n\n  - label: Mongo\n    type: '
           b'mongo-default'
           b'\n\ntrustzones:\n\n  - label: Internet Boundary\n    type: f0ba7722-39b6-4c81-8290-a30a248bb8d9'
           b'\n\n  - label: Public Cloud\n    type: b61d6911-338d-46a8-9f39-8dcd24abfe91'
           b'\n\nconfiguration:\n\n  value_a: default_value_a\n\n  value_b: default_value_b'
           b'\n\n  my_list:\n  - a\n  - b\n  - c\n')
custom = (b'components:\n\n  - label: AmazonEC2\n    type: ec2-custom\n\n  - label: Postgres\n    type: '
          b'psql-custom'
          b'\n\ntrustzones:\n\n  - label: Internet Boundary\n    type: 6376d53e-6461-412b-8e04-7b3fe2b397de'
          b'\n\n  - label: Public Cloud\n    type: 2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
          b'\n\nconfiguration:\n\n  value_a: custom_value_a\n\n  value_c: custom_value_c'
          b'\n\n  my_list:\n  - a\n  - y\n  - z\n')


class TestMappingFileLoader:

    def test_mapping_file_priority(self):
        # GIVEN the mapping loader with a default and custom mapping files
        mapping_file_loader = MappingFileLoader([default, custom])

        # WHEN load is called in MappingFileLoader
        mapping_file = mapping_file_loader.load()

        # THEN the result has the expected components
        assert len(mapping_file['components']) == 4
        # AND the first components are the custom ones
        assert mapping_file['components'][0] == {'label': 'AmazonEC2', 'type': 'ec2-custom'}
        assert mapping_file['components'][1] == {'label': 'Postgres', 'type': 'psql-custom'}
        # AND the last components are the default ones
        assert mapping_file['components'][2] == {'label': 'Postgres', 'type': 'psql-default'}
        assert mapping_file['components'][3] == {'label': 'Mongo', 'type': 'mongo-default'}

        # AND  the result has the expected trust zones
        assert len(mapping_file['trustzones']) == 4
        # AND the first trust zones are the default ones as well
        assert mapping_file['trustzones'][0] == {'label': 'Internet Boundary',
                                                 'type': '6376d53e-6461-412b-8e04-7b3fe2b397de'}
        assert mapping_file['trustzones'][1] == {'label': 'Public Cloud',
                                                 'type': '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'}
        # AND the last trust zones are the custom ones as well
        assert mapping_file['trustzones'][2] == {'label': 'Internet Boundary',
                                                 'type': 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'}
        assert mapping_file['trustzones'][3] == {'label': 'Public Cloud',
                                                 'type': 'b61d6911-338d-46a8-9f39-8dcd24abfe91'}

        # AND the configuration has three values
        assert len(mapping_file['configuration']) == 4
        # AND configuration with value_a is override by the custom file
        assert mapping_file['configuration']['value_a'] == 'custom_value_a'
        # AND configuration with value_b gets its value from default
        assert mapping_file['configuration']['value_b'] == 'default_value_b'
        # AND configuration with value_c gets its value from custom
        assert mapping_file['configuration']['value_c'] == 'custom_value_c'
        # AND configuration with the list has all elements
        assert mapping_file['configuration']['my_list'] == ['a', 'y', 'z', 'a', 'b', 'c']

    @mark.parametrize('default_config, custom_config,expected_client,expected_tz,expected_skip', [
        param(
            b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client\n\n    trustzone: f0ab',
            b'\n\nconfiguration:\n\n  skip:\n\n    - ec2\n\n    - s3\n\n    - iam\n\n',
            'generic-client',
            'f0ab',
            ['ec2', 's3', 'iam'],
            id='default_attack_custom_skip'),
        param(b'\n\nconfiguration:\n\n  skip:\n\n    - ec2\n\n    - s3\n\n    - iam\n\n',
              b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client\n\n    trustzone: f0ab',
              'generic-client',
              'f0ab',
              ['ec2', 's3', 'iam'],
              id='default_skip_custom_attack'),
        param(b'\n\nconfiguration:\n\n  skip:\n\n    - ec2\n\n    - s3\n\n    - iam\n\n',
              b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client\n\n    trustzone: f0ab'
              b'\n\n  skip:\n\n    - mongo\n\n    - postgres\n\n    - iam',
              'generic-client',
              'f0ab',
              ['mongo', 'postgres', 'iam', 'ec2', 's3', 'iam'],
              id='both_skip_custom_attack'),
        param(b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client\n\n    trustzone: f0ab'
              b'\n\n  skip:\n\n    - ec2\n\n    - s3\n\n    - iam\n\n',
              b'\n\nconfiguration:\n\n  skip:\n\n    - mongo\n\n    - postgres\n\n    - iam',
              'generic-client',
              'f0ab',
              ['mongo', 'postgres', 'iam', 'ec2', 's3', 'iam'],
              id='both_skip_default_attack'),
        param(b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client\n\n    trustzone: f0ab'
              b'\n\n  skip:\n\n    - ec2\n\n    - s3\n\n    - iam\n\n',
              b'\n\nconfiguration:\n\n  attack_surface:\n    client: generic-client-custom\n\n    trustzone: d1ab'
              b'\n\n  skip:\n\n    - mongo\n\n    - postgres\n\n    - iam',
              'generic-client-custom',
              'd1ab',
              ['mongo', 'postgres', 'iam', 'ec2', 's3', 'iam'],
              id='both_skip_both_attack'),
    ])
    def test_override_configuration(self, default_config, custom_config, expected_client, expected_tz, expected_skip):
        # GIVEN the mapping loader with a default and custom mapping files configurations
        mapping_file_loader = MappingFileLoader([default_config, custom_config])

        # WHEN load is called in MappingFileLoader
        mapping_file = mapping_file_loader.load()

        # THEN attack_surface configuration has the expected values
        assert mapping_file['configuration']['attack_surface']['client'] == expected_client
        assert mapping_file['configuration']['attack_surface']['trustzone'] == expected_tz
        # AND the skip configuration has the expected values
        assert mapping_file['configuration']['skip'] == expected_skip
