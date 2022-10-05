from click.testing import CliRunner
from pytest import mark

from slp_base import LoadingIacFileError, MappingFileNotValidError
from slp_base.tests.util.otm import validate_and_diff
from startleft.startleft.cli.cli import parse_any
from tests.integration.cli.parse.iac.test_cli_parse_iac import excluded_regex
from tests.resources import test_resource_paths
from tests.resources.test_resource_paths import invalid_tf

# mappings
TERRAFORM_VALID_MAPPING_FILENAME = test_resource_paths.default_terraform_aws_mapping
TERRAFORM_WRONG_ID_MAPPING_FILENAME = test_resource_paths.terraform_malformed_mapping_wrong_id
# IaC files
TERRAFORM_AWS_SIMPLE_COMPONENTS = test_resource_paths.terraform_aws_simple_components
TERRAFORM_UNKNOWN_RESOURCE = test_resource_paths.terraform_unknown_resource
TERRAFORM_UNKNOWN_MODULE = test_resource_paths.terraform_unknown_module
# otm
OTM_AWS_SIMPLE_COMPONENTS_EXPECTED = test_resource_paths.terraform_aws_simple_components_otm_expected
OTM_EMPTY_FILE = test_resource_paths.otm_empty_file_example


class TestCliParseIaCTerraform:
    """
    The testing for click parse commands for TERRAFORM files
    """

    def test_parse_terraform_file_ok(self):
        """
        Parsing Terraform file wih a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "TERRAFORM",
                #   and a valid mapping terraform file
                '--mapping-file', TERRAFORM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "test_parse_terraform_file_ok",
                #   and a valid project id
                '--project-id', "test_parse_terraform_file_ok",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TERRAFORM_AWS_SIMPLE_COMPONENTS]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff(output_file_name, OTM_AWS_SIMPLE_COMPONENTS_EXPECTED, excluded_regex) == {}

    def test_parse_terraform_unknown_resources(self):
        """
        Parsing Terraform file wih unknown resources
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "TERRAFORM",
                #   and a valid mapping terraform file
                '--mapping-file', TERRAFORM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TERRAFORM_UNKNOWN_RESOURCE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff(output_file_name, OTM_EMPTY_FILE, excluded_regex) == {}

    def test_parse_terraform_unknown_module(self):
        """
        Parsing Terraform file wih an unknown module
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "TERRAFORM",
                #   and a valid mapping terraform file
                '--mapping-file', TERRAFORM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TERRAFORM_UNKNOWN_MODULE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff(output_file_name, OTM_EMPTY_FILE, excluded_regex) == {}

    @mark.parametrize('filename', [invalid_tf])
    def test_parse_terraform_invalid_file(self, filename):
        """
        Parsing invalid terraform file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "TERRAFORM",
                #   and a valid mapping terraform file
                '--mapping-file', TERRAFORM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                filename]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then a LoadingIacFileError is returned
            assert isinstance(result.exception, LoadingIacFileError)

    @mark.parametrize('mapping_file', [TERRAFORM_WRONG_ID_MAPPING_FILENAME])
    def test_parse_terraform_invalid_mapping_file(self, mapping_file):
        """
        Parse with an invalid Mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "TERRAFORM",
                #   and a valid mapping terraform file
                '--mapping-file', mapping_file,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TERRAFORM_AWS_SIMPLE_COMPONENTS]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then a MappingFileNotValidError is returned
            assert isinstance(result.exception, MappingFileNotValidError)
