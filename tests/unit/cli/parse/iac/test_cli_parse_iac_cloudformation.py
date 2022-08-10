import logging
from unittest.mock import patch

from click.testing import CliRunner

from startleft.cli import parse_any
from tests.resources import test_resource_paths

CLOUDFORMATION_MAPPING = test_resource_paths.default_cloudformation_mapping
CLOUDFORMATION_FOR_MAPPING_TESTS = test_resource_paths.cloudformation_for_mappings_tests_json


class TestCliParseIaCCloudformation:

    @patch('startleft.cli.parse_iac')
    def test_parse_cloudformation_file_ok(self, mock, caplog):
        """
        Parsing Cloudformation file wih a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', "CLOUDFORMATION",
                #   and a valid mapping file
                '--mapping-file', CLOUDFORMATION_MAPPING,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                CLOUDFORMATION_FOR_MAPPING_TESTS]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()
