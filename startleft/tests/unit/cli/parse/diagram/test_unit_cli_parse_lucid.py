import logging
from unittest.mock import patch
from pytest import mark

from click.testing import CliRunner

from startleft.startleft.cli.cli import parse_any
from startleft.tests.resources import test_resource_paths

TESTING_LUCID_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_lucid_mapping
TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_FILENAME = test_resource_paths.custom_lucid_mapping_with_tz
TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_AND_VPC_FILENAME = test_resource_paths.custom_lucid_mapping_with_tz_and_vpc

TESTING_VALID_LUCID_FILE_WITH_TZ = test_resource_paths.lucid_aws_with_tz
TESTING_VALID_LUCID_FILE_WITH_TZ_AND_VPC = test_resource_paths.lucid_aws_with_tz_and_vpc

TESTING_DIAGRAM_TYPE = 'LUCID'
OUTPUT_FILE_NAME = "output-file.otm"


class TestCliParseLucid:

    @patch('startleft.startleft.cli.cli.parse_diagram')
    def test_lucid_parse_successful_without_custom_mapping_file(self, mock, caplog):
        """
        Parsing Lucid file with a valid mapping file
        """
        runner = CliRunner()
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with a valid Lucidchart file and a valid default mapping file
            args = [
                # a valid Lucid type
                '--diagram-type', TESTING_DIAGRAM_TYPE,
                #   and a valid default mapping file
                '--default-mapping-file', TESTING_LUCID_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', OUTPUT_FILE_NAME,
                #   and a valid input file
                TESTING_VALID_LUCID_FILE_WITH_TZ]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    @patch('startleft.startleft.cli.cli.parse_diagram')
    @mark.parametrize('input_file, custom_mapping_file', [
        (TESTING_VALID_LUCID_FILE_WITH_TZ, TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_FILENAME),
        (TESTING_VALID_LUCID_FILE_WITH_TZ_AND_VPC, TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_AND_VPC_FILENAME),
    ])
    def test_lucid_parse_successful_with_custom_mapping_file(self, mock, caplog, input_file, custom_mapping_file):
        """
        Parsing Lucid file with an invalid commands options
        """
        runner = CliRunner()
        caplog.set_level(logging.INFO)

        with runner.isolated_filesystem():
            # Given a list of arguments with a valid Lucidchart file, a valid default mapping file and a valid custom
            # mapping file
            args = [
                # a valid Lucid type
                '--diagram-type', TESTING_DIAGRAM_TYPE,
                #   and a valid default mapping file
                '--default-mapping-file', TESTING_LUCID_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid custom mapping file
                '--custom-mapping-file', custom_mapping_file,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', OUTPUT_FILE_NAME,
                #   and a valid input file
                input_file]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()

    @mark.parametrize('processor_type_option, processor_type_name, mapping_file_option, mapping_file', [
        ('--iac-type', 'TERRAFORM', '', '')
    ])
    def test_lucid_parse_incompatible_parameters_error(self, processor_type_option, processor_type_name,
                                                       mapping_file_option, mapping_file):
        """
        Parsing Lucid file with an invalid commands options
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', TESTING_DIAGRAM_TYPE,
                # a valid type
                processor_type_option, processor_type_name,
                #   and a mapping file
                mapping_file_option, mapping_file,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', OUTPUT_FILE_NAME,
                #   and a valid input file
                TESTING_VALID_LUCID_FILE_WITH_TZ]

            # When parse command is called
            result = runner.invoke(parse_any, args)

            # THEN a 2 exit code is returned
            assert result.exit_code == 2

            assert result.stdout.__contains__("Error: Invalid arguments: diagram_type is incompatible with:")
            assert result.stdout.__contains__("etm_type")
            assert result.stdout.__contains__("iac_type")
