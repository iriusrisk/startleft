import logging
from unittest.mock import patch

from click.testing import CliRunner

# mappings
from startleft.cli import parse_any
from tests.resources import test_resource_paths

TESTING_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_visio_mapping
TESTING_CUSTOM_VALID_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
# diagrams
TESTING_VALID_DIAGRAM_FILE = test_resource_paths.visio_aws_with_tz_and_vpc

TESTING_DIAGRAM_TYPE = 'VISIO'

class TestCliParseDiagram:

    @patch('startleft.cli.parse_diagram')
    def test_parse_diagram_file_ok(self, mock, caplog):
        """
        Parsing Diagram file with a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', TESTING_DIAGRAM_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_DIAGRAM_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    def test_parse_diagram_mutually_exclusion_error(self):
        """
        Parsing Diagram file with an invalid commands options
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', TESTING_DIAGRAM_TYPE,
                # a valid IaC type
                '--iac-type', "CLOUDFORMATION",
                #   and a valid mapping file
                '--default-mapping-file', TESTING_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_DIAGRAM_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 2

            assert result.stdout.__contains__("Error: Invalid arguments: diagram_type is incompatible with:")
            assert result.stdout.__contains__("mapping_file")
            assert result.stdout.__contains__("iac_type")
