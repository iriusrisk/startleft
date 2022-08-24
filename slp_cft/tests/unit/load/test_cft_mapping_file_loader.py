from unittest import TestCase
from unittest.mock import patch

from deepmerge import always_merger

from slp_cft.slp_cft.load.cft_mapping_file_loader import CloudformationMappingFileLoader
from slp_base.slp_base.errors import LoadingMappingFileError


class TestCloudformationMappingFileLoader(TestCase):

    @patch('yaml.load')
    def test_single_valid_file(self, yaml_load_mock):
        # GIVEN a single valid CloudFormation mapping file
        mapping_file_data = [bytes('VALID CFT FILE', 'utf-8')]

        # AND a mock for the yaml.load method
        mappings_result = {'key': 'value'}
        yaml_load_mock.side_effect = [mappings_result]

        # WHEN the load method is called
        mappings = CloudformationMappingFileLoader(mapping_file_data).load()

        # THEN a dictionary with the file mappings is returned
        yaml_load_mock.assert_called()
        assert mappings == mappings_result

    @patch('yaml.load')
    def test_multiple_valid_files(self, yaml_load_mock):
        # GIVEN two valid CloudFormation mapping file
        mapping_file_data = [bytes('VALID CFT FILE', 'utf-8'), bytes('VALID CFT FILE', 'utf-8')]

        # AND a mock for the yaml.load method
        first_file_mappings = {'key_from_first': 'value_from_first'}
        second_file_mappings = {'key_from_second': 'value_from_second'}
        yaml_load_mock.side_effect = [first_file_mappings, second_file_mappings]

        # WHEN the load method is called
        mappings = CloudformationMappingFileLoader(mapping_file_data).load()

        # THEN both mapping files are processed
        assert yaml_load_mock.call_count == 2

        # AND a dictionary with all the mappings is returned
        assert mappings == always_merger.merge(first_file_mappings, second_file_mappings)

    @patch('yaml.load')
    def test_invalid_file(self, yaml_load_mock):
        # GIVEN an invalid CloudFormation mapping file
        mapping_file_data = [bytes('INVALID CFT FILE', 'utf-8')]

        # AND a mock of the hcl2 load function that returns an error
        yaml_load_error_msg = 'Cannot process given mapping file.'
        yaml_load_mock.side_effect = Exception(yaml_load_error_msg)

        # WHEN load function is called
        # THEN a LoadingMappingFileError is raised
        with self.assertRaises(LoadingMappingFileError) as loading_error:
            CloudformationMappingFileLoader(mapping_file_data).load()

        # AND The error info is right
        assert str(loading_error.exception.title) == 'Error loading the CFT mapping file. The mapping files are not valid.'
        assert str(loading_error.exception.message) == yaml_load_error_msg

    def test_no_mapping_files(self):
        # GIVEN no mapping files
        mapping_file_data = []

        # WHEN the load method is called
        # THEN a LoadingMappingFileError is raised
        with self.assertRaises(LoadingMappingFileError) as loading_error:
            CloudformationMappingFileLoader(mapping_file_data).load()

        # AND an empty mapping file message is on the exception
        assert str(loading_error.exception.title) == 'Mapping file is not valid'
        assert str(loading_error.exception.message) == 'Mapping file is empty'

    def test_empty_mapping_file(self):
        # GIVEN an empty mapping_file
        mapping_file_data = [bytes('', 'utf-8')]

        # WHEN the load method is called
        mappings = CloudformationMappingFileLoader(mapping_file_data).load()

        # THEN no mappings are returned
        assert mappings == {}

    @patch('yaml.load')
    def test_some_empty_mapping_file(self, yaml_load_mock):
        # GIVEN an empty and a non empty mapping file
        mapping_file_data = [bytes('VALID CFT FILE', 'utf-8'), bytes('', 'utf-8')]

        # AND a mock for the yaml.load method
        mappings_result = {'key': 'value'}
        yaml_load_mock.side_effect = [mappings_result]

        # WHEN the load method is called
        mappings = CloudformationMappingFileLoader(mapping_file_data).load()

        # THEN only one mapping file is processed
        assert yaml_load_mock.call_count == 1

        # AND a dictionary with the file mappings is returned
        assert mappings == mappings_result

