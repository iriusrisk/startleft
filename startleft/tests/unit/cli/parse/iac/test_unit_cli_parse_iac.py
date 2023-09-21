import logging
from unittest.mock import patch

from click.testing import CliRunner

from startleft.startleft.cli.cli import parse_any
from tests.integration.cli.parse.iac.cloudformation.test_cli_parse_iac_cloudformation import \
    CLOUDFORMATION_MAPPING, \
    CLOUDFORMATION_FOR_MAPPING_TESTS

TESTING_IAC_TYPE = 'CLOUDFORMATION'
TESTING_IAC_FILE = CLOUDFORMATION_FOR_MAPPING_TESTS
TESTING_MAPPING_FILE = CLOUDFORMATION_MAPPING


class TestCliParseIaCCloudformation:

    @patch('startleft.startleft.cli.cli.parse_iac')
    def test_parse_cloudformation_file_ok(self, mock, caplog):
        """
        Parsing Cloudformation file with a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_MAPPING_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_IAC_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    def test_parse_cloudformation_mutually_exclusion_error(self):
        """
        Parsing Cloudformation file with an invalid commands options
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', TESTING_MAPPING_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_IAC_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 2

            assert result.stdout.__contains__("Error: Invalid arguments: iac_type is incompatible with:")
            assert result.stdout.__contains__("etm_type")
            assert result.stdout.__contains__("diagram_type")
