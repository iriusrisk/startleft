from unittest import TestCase
from unittest.mock import patch

from numpy import random

from startleft.api.errors import IacFileNotValidError
from startleft.processors.terraform.validate.tf_validator import TerraformValidator

VALID_MIME = 'text/plain'
MIN_SIZE = 20
MAX_SIZE = 20 * 1024 * 1024


def create_terraform_file_data(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


class TestTerraformValidator(TestCase):

    @patch('magic.Magic.from_buffer')
    def test_valid_file(self, mime_checker_mock):
        # GIVEN a TF source with right size
        source = create_terraform_file_data(size=random.randint(MIN_SIZE, MAX_SIZE))

        # AND a mock for the mime checker returning a valid MIME
        mime_checker_mock.side_effect = [VALID_MIME]

        # WHEN the validate method
        TerraformValidator(source).validate()

        # THEN file is checked and no exception raised
        mime_checker_mock.assert_called()

    def test_invalid_size_file(self):
        # GIVEN a TF source with an invalid size
        source = create_terraform_file_data(size=10)

        # WHEN the validate method
        # THEN an IacFileNotValidError is raised
        with self.assertRaises(IacFileNotValidError) as validation_error:
            TerraformValidator(source).validate()

        # AND the right info is in the exception
        assert validation_error.exception.title == 'Terraform file is not valid'
        assert validation_error.exception.message == 'Provided Terraform file is not valid. Invalid size'

    @patch('magic.Magic.from_buffer')
    def test_invalid_mime_type_file(self, mime_checker_mock):
        # GIVEN a TF source with right size
        source = create_terraform_file_data(size=random.randint(MIN_SIZE, MAX_SIZE))

        # AND a mock for the mime checker returning and invalid MIME
        mime_checker_mock.side_effect = ['Invalid MIME']

        # WHEN the validate method
        # THEN an IacFileNotValidError is raised
        with self.assertRaises(IacFileNotValidError) as validation_error:
            TerraformValidator(source).validate()

        # AND the right info is in the exception
        assert validation_error.exception.title == 'Terraform file is not valid'
        assert validation_error.exception.message == 'Invalid content type for Terraform file'








