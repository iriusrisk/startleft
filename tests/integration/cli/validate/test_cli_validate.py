import logging
import pytest

from click.testing import CliRunner

from startleft.startleft.cli.cli import validate
from tests.resources import test_resource_paths

SAMPLE_OTM_FILENAME = test_resource_paths.otm_file_example
SAMPLE_OTM_YAML_FILENAME = test_resource_paths.otm_yaml_file_example
CFT_VALID_MAPPING_FILENAME = test_resource_paths.default_cloudformation_mapping
INVALID_YAML_FILENAME = test_resource_paths.invalid_yaml
CUSTOM_YAML_VISIO_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
MTMT_MAPPING_FILENAME_VALID = test_resource_paths.mtmt_mapping_file_valid
MTMT_MAPPING_FILENAME_INVALID = test_resource_paths.mtmt_mapping_file_invalid
VISIO_VALID_MAPPING_FILE = test_resource_paths.default_visio_mapping
LUCID_VALID_MAPPING_FILE = test_resource_paths.default_lucid_mapping
TF_VALID_MAPPING_FILE = test_resource_paths.terraform_iriusrisk_tf_aws_mapping
TF_INVALID_MAPPING_FILE = test_resource_paths.terraform_malformed_mapping_wrong_id


class TestCliValidate:
    """
    The testing for click validate commands
    """
    def test_validate_otm_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a valid OTM file
        result = runner.invoke(validate, ['--otm-file', SAMPLE_OTM_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating OTM is performed
        assert 'Validating OTM file' in caplog.text
        #   and validation OTM finish successfully
        assert 'OTM file validated successfully' in caplog.text

    def test_validate_otm_yaml_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a valid OTM file in YAML format
        result = runner.invoke(validate, ['--otm-file', SAMPLE_OTM_YAML_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating OTM is performed
        assert 'Validating OTM file' in caplog.text
        #   and validation OTM finish successfully
        assert 'OTM file validated successfully' in caplog.text

    def test_validate_valid_otm_file_with_invalid_arguments(self):
        """
        Validating valid otm file with mapping-type argument
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid otm file
                '--otm-file', SAMPLE_OTM_FILENAME,
                # and a valid mapping type
                '--mapping-type', 'VISIO']

            # When validating
            result = runner.invoke(validate, args)

            # Then the exit code is 2
            assert result.exit_code == 2
            # And an invalid arguments message is displayed
            assert result.stdout.__contains__("Error: Invalid arguments: mapping_type is incompatible with: otm_file")

    @pytest.mark.parametrize('mapping_file, mapping_file_type', [
        pytest.param(VISIO_VALID_MAPPING_FILE, 'VISIO', id="with a valid VISIO mapping file"),
        pytest.param(MTMT_MAPPING_FILENAME_VALID, 'MTMT', id="with a valid MTMT mapping file"),
        pytest.param(CFT_VALID_MAPPING_FILENAME, 'CLOUDFORMATION', id="with a valid CLOUDFORMATION mapping file"),
        pytest.param(LUCID_VALID_MAPPING_FILE, 'LUCID', id="with a valid LUCID mapping file"),
        pytest.param(TF_VALID_MAPPING_FILE, 'TERRAFORM', id="with a valid TERRAFORM mapping file")])
    def test_validate_valid_mapping_files(self, mapping_file, mapping_file_type, caplog):
        """
        Validating valid mapping files
        """
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid mapping file
                '--mapping-file', mapping_file,
                #   and a valid mapping file type
                '--mapping-type', mapping_file_type]

            # When validating
            result = runner.invoke(validate, args)

            # Then the result of the validation is correct
            assert result.exit_code == 0
            #   and validating mapping file is performed
            assert f'Validating: {mapping_file_type} mapping files' in caplog.text
            #   and validation finishes successfully
            assert 'Mapping files are valid' in caplog.text

    @pytest.mark.parametrize('mapping_file, mapping_file_type', [
        pytest.param(MTMT_MAPPING_FILENAME_INVALID, 'MTMT', id="with an invalid MTMT mapping file"),
        pytest.param(INVALID_YAML_FILENAME, 'CLOUDFORMATION', id="with an invalid CLOUDFORMATION mapping file"),
        pytest.param(INVALID_YAML_FILENAME, 'VISIO', id="with an invalid VISIO mapping file"),
        pytest.param(TF_INVALID_MAPPING_FILE, 'LUCID', id="with an invalid LUCID mapping file"),
        pytest.param(TF_INVALID_MAPPING_FILE, 'TERRAFORM', id="with an invalid TERRAFORM mapping file")])
    def test_validate_invalid_mapping_files(self, mapping_file, mapping_file_type, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating an invalid mapping file
        result = runner.invoke(validate, ['--mapping-file', mapping_file,
                                          '--mapping-type', mapping_file_type])

        # Then validator returns not OK
        assert result.exit_code == 1
        #   and validation is performed
        assert f'Validating: {mapping_file_type} mapping files' in caplog.text
        #   and validation ETM finish unsuccessfully
        assert 'Mapping file is not valid' in caplog.text
        # AND the error code is 22
        assert result.exception.error_code.system_exit_status == 22

    def test_validate_command_with_both_mapping_file_and_otm_file_arguments(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid mapping file
                '--mapping-file', CFT_VALID_MAPPING_FILENAME,
                # and a valid otm file
                '--otm-file', SAMPLE_OTM_FILENAME]

            # When validating
            result = runner.invoke(validate, args)

            # Then the exit code is 2
            assert result.exit_code == 2
            assert result.stdout.__contains__("Invalid arguments")
            assert result.stdout.__contains__("mapping_file")
            assert result.stdout.__contains__("otm_file")

    def test_validate_command_without_mapping_file_argument(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid mapping type
                # and without mapping-file argument
                '--mapping-type', 'MTMT']

            # When validating
            result = runner.invoke(validate, args)

            # Then the exit code is 2
            assert result.exit_code == 2
            assert result.stdout.__contains__("Error: Missing one of this arguments: ")
            assert result.stdout.__contains__("mapping_file")
            assert result.stdout.__contains__("otm_file")

    def test_validate_command_without_type_argument(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid mapping file
                # and without mapping-type argument
                '--mapping-file', CFT_VALID_MAPPING_FILENAME]

            # When validating
            result = runner.invoke(validate, args)

            # Then the exit code is 2
            assert result.exit_code == 2
            assert result.stdout.__contains__("Error: Missing one of this arguments: ")
            assert result.stdout.__contains__("mapping_type")
            assert result.stdout.__contains__("otm_file")

    @pytest.mark.parametrize('mapping_file, mapping_file_type', [
        pytest.param(MTMT_MAPPING_FILENAME_VALID, 'CLOUDFORMATION', id="with a valid MTMT mapping file and an invalid "
                                                                       "CLOUDFORMATION type"),
        pytest.param(VISIO_VALID_MAPPING_FILE, 'TERRAFORM', id="with a valid VISIO mapping file and an invalid "
                                                               "TERRAFORM type"),
        pytest.param(CFT_VALID_MAPPING_FILENAME, 'VISIO',
                     id="with a valid CLOUDFORMATION mapping file and an invalid VISIO type"),
        pytest.param(LUCID_VALID_MAPPING_FILE, 'TERRAFORM',
                     id="with a valid LUCID mapping file and an invalid TERRAFORM type"),
        pytest.param(TF_VALID_MAPPING_FILE, 'MTMT', id="with a valid TERRAFORM mapping file and an invalid MTMT type")])
    def test_validate_valid_mapping_file_and_invalid_type(self, mapping_file, mapping_file_type):
        """
        Validating valid mapping files
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid mapping file
                '--mapping-file', mapping_file,
                #   and a valid mapping file type
                '--mapping-type', mapping_file_type]

            # When validating
            result = runner.invoke(validate, args)

            # Then the exit code is 1
            assert result.exit_code == 1
            # AND the error code is 22
            assert result.exception.error_code.system_exit_status == 22
            assert result.exception.args[0] == 'Mapping files are not valid'

    @pytest.mark.parametrize('mapping_file_type', ['PDF', 'ZIP'])
    def test_validate_valid_mapping_file_and_wrong_type(self, mapping_file_type):
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid CFT mapping file
                '--mapping-file', CFT_VALID_MAPPING_FILENAME,
                #   and a wrong mapping file type
                '--mapping-type', mapping_file_type]

            # When validating
            result = runner.invoke(validate, args)
            # Then the exit code is 2
            assert result.exit_code == 2
            assert result.stdout.__contains__("Error: Invalid value for '--mapping-type' / '-t'")
            assert result.stdout.__contains__(mapping_file_type)
