from unittest import TestCase
from unittest.mock import patch

from startleft.api.errors import LoadingIacFileError
from startleft.processors.terraform.load.tf_loader import TerraformLoader


class TestTerraformLoader(TestCase):

    @patch('hcl2.load')
    def test_valid_hcl2(self, hcl2_mock):
        # GIVEN a mocked valid hcl2 source
        source = 'VALID TERRAFORM FILE SOURCE'

        # AND a mock of the hcl2 load function
        hcl2_load_result = {'resource': {'name': 'tf_resource'}}
        hcl2_mock.side_effect = [hcl2_load_result]

        # WHEN load function is called
        tf_loader = TerraformLoader(source)
        tf_loader.load()

        # THEN a dict with the Terraform data is built
        hcl2_mock.assert_called()
        assert tf_loader.get_terraform() == hcl2_load_result

    @patch('hcl2.load')
    def test_invalid_hcl2(self, hcl2_mock):
        # GIVEN an invalid hcl2 source
        source = 'INVALID TERRAFORM FILE SOURCE'

        # AND a mock of the hcl2 load function that returns an error
        hcl2_load_error_msg = 'Cannot process given TF file.'
        hcl2_mock.side_effect = Exception(hcl2_load_error_msg)

        # WHEN load function is called
        # THEN a LoadingIacFileError is raised
        tf_loader = TerraformLoader(source)
        with self.assertRaises(LoadingIacFileError) as loading_error:
            tf_loader.load()

        # AND The error info is right
        assert str(loading_error.exception.title) == 'IaC file is not valid'
        assert str(loading_error.exception.message) == hcl2_load_error_msg

    def test_empty_file(self):
        pass
        # GIVEN an empty hcl2 source
        source = ''

        # WHEN load function is called
        # THEN a LoadingIacFileError is raised
        tf_loader = TerraformLoader(source)
        with self.assertRaises(LoadingIacFileError) as loading_error:
            tf_loader.load()

        # AND an empty IaC file message is on the exception
        assert str(loading_error.exception.title) == 'IaC file is not valid'
        assert str(loading_error.exception.message) == 'IaC file is empty'
