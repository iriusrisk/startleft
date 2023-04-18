from unittest import TestCase
from unittest.mock import patch

from slp_base import IacFileNotValidError
from slp_tf.slp_tf.validate.tf_validator import TerraformValidator

VALID_MIME = 'text/plain'
MIN_SIZE = 20
MAX_SIZE = 1000000 # 1MB


def create_terraform_file_data(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


class TestTerraformValidator(TestCase):

    @patch('magic.Magic.from_buffer')
    def test_valid_file(self, mime_checker_mock):
        # GIVEN a TF source with right size
        source = create_terraform_file_data(size=100)

        # AND a mock for the mime checker returning a valid MIME
        mime_checker_mock.side_effect = [VALID_MIME]

        # WHEN the validate method
        TerraformValidator([source]).validate()

        # THEN file is checked and no exception raised
        mime_checker_mock.assert_called()

    def test_invalid_size_file(self):
        # GIVEN a TF source with an invalid size
        source = create_terraform_file_data(size=10)

        # WHEN the validate method
        # THEN an IacFileNotValidError is raised
        with self.assertRaises(IacFileNotValidError) as validation_error:
            TerraformValidator([source]).validate()

        # AND the right info is in the exception
        assert validation_error.exception.title == 'Terraform file is not valid'
        assert validation_error.exception.message == 'Provided iac_file is not valid. Invalid size'

    @patch('magic.Magic.from_buffer')
    def test_invalid_mime_type_file(self, mime_checker_mock):
        # GIVEN a TF source with right size
        source = create_terraform_file_data(size=100)

        # AND a mock for the mime checker returning and invalid MIME
        mime_checker_mock.side_effect = ['Invalid MIME']

        # WHEN the validate method
        # THEN an IacFileNotValidError is raised
        with self.assertRaises(IacFileNotValidError) as validation_error:
            TerraformValidator([source]).validate()

        # AND the right info is in the exception
        assert validation_error.exception.title == 'Terraform file is not valid'
        assert validation_error.exception.message == 'Invalid content type for iac_file'
