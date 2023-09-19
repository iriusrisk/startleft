import logging
from unittest.mock import patch
from pytest import mark

from click.testing import CliRunner

# mappings
from startleft.startleft.cli.cli import parse_any
from startleft.tests.resources import test_resource_paths

TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_mtmt_mapping
TESTING_MTMT_CUSTOM_VALID_MAPPING_FILENAME = test_resource_paths.custom_mtmt_mapping
# etm valid file
TESTING_VALID_ETM_FILE = test_resource_paths.mtmt_mobile_api_example
TESTING_VALID_CUSTOM_ETM_FILE = test_resource_paths.mtmt_mobile_custom_api_example

TESTING_ETM_TYPE = 'MTMT'


class TestCliParseEtm:

    @patch('startleft.startleft.cli.cli.parse_etm')
    def test_etm_parse_successful_without_custom_mapping_file(self, mock, caplog):
        """
        Parsing MTMT file with a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with a valid MTMT file and a valid default mapping file
            args = [
                # a valid Etm type
                '--etm-type', TESTING_ETM_TYPE,
                #   and a valid default mapping file
                '--default-mapping-file', TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_ETM_FILE]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    @patch('startleft.startleft.cli.cli.parse_etm')
    def test_etm_parse_successful_with_custom_mapping_file(self, mock, caplog):
        """
        Parsing MTMT file with an invalid commands options
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with a valid MTMT file, a valid default mapping file and a valid custom
            # mapping file
            args = [
                # a valid Etm type
                '--etm-type', TESTING_ETM_TYPE,
                #   and a valid default mapping file
                '--default-mapping-file', TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid custom mapping file
                '--custom-mapping-file', TESTING_MTMT_CUSTOM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_CUSTOM_ETM_FILE]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    @mark.parametrize('processor_type_option, processor_type_name, mapping_file_option, mapping_file', [
        ('--diagram-type', 'VISIO', '', ''),
        ('--iac-type', 'TERRAFORM', '', ''),
    ])
    def test_etm_parse_incompatible_parameters_error(self, processor_type_option, processor_type_name,
                                                     mapping_file_option, mapping_file):
        """
        Parsing MTMT file with an invalid commands options
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Etm type
                '--etm-type', TESTING_ETM_TYPE,
                # a valid type
                processor_type_option, processor_type_name,
                #   and a mapping file
                mapping_file_option, mapping_file,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_ETM_FILE]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # THEN a 2 exit code is returned
            assert result.exit_code == 2

            assert result.stdout.__contains__("Error: Invalid arguments: etm_type is incompatible with:")
            assert result.stdout.__contains__("iac_type")
            assert result.stdout.__contains__("diagram_type")


