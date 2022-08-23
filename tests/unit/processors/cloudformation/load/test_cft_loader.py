from unittest import TestCase
from unittest.mock import patch

from startleft.api.errors import LoadingIacFileError
from startleft.processors.cloudformation.load.cft_loader import CloudformationLoader


class TestCloudformationLoader(TestCase):

    @patch('yaml.load')
    def test_valid_cft(self, yaml_mock):
        # GIVEN a mocked valid yaml source
        source = 'VALID CLOUDFORMATION FILE SOURCE'

        # AND a mock of the yaml load function
        yaml_load_result = {'resource': {'name': 'cft_resource'}}
        yaml_mock.side_effect = [yaml_load_result]

        # WHEN load function is called
        cft_loader = CloudformationLoader(source)
        cft_loader.load()

        # THEN a dict with the Cloudformation data is built
        yaml_mock.assert_called()
        assert cft_loader.get_cloudformation() == yaml_load_result

    @patch('yaml.load')
    def test_invalid_cft(self, yaml_mock):
        # GIVEN an invalid yaml source
        source = 'INVALID CLOUDFORMATION FILE SOURCE'

        # AND a mock of the yaml load function that returns an error
        yaml_load_error_msg = 'Cannot process given CFT file.'
        yaml_mock.side_effect = Exception(yaml_load_error_msg)

        # WHEN load function is called
        # THEN a LoadingIacFileError is raised
        cft_loader = CloudformationLoader(source)
        with self.assertRaises(LoadingIacFileError) as loading_error:
            cft_loader.load()

        # AND The error info is right
        assert str(loading_error.exception.title) == 'IaC file is not valid'
        assert str(loading_error.exception.message) == yaml_load_error_msg

    def test_empty_file(self):
        pass
        # GIVEN an empty yaml source
        source = ''

        # WHEN load function is called
        # THEN a LoadingIacFileError is raised
        cft_loader = CloudformationLoader(source)
        with self.assertRaises(LoadingIacFileError) as loading_error:
            cft_loader.load()

        # AND an empty IaC file message is on the exception
        assert str(loading_error.exception.title) == 'IaC file is not valid'
        assert str(loading_error.exception.message) == 'IaC file is empty'
