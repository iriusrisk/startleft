from unittest.mock import patch
from pytest import mark

from click.testing import CliRunner

from slp_base.slp_base.errors import MappingFileNotValidError, SourceFileNotValidError, LoadingSourceFileError
from startleft.startleft.cli.cli import parse_any
from startleft.tests.resources import test_resource_paths

TESTING_ETM_TYPE = 'MTMT'
# mappings
TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_mtmt_mapping
TESTING_MTMT_CUSTOM_VALID_MAPPING_FILENAME = test_resource_paths.custom_mtmt_mapping
TESTING_MTMT_INVALID_MAPPING_FILENAME = test_resource_paths.invalid_mtmt_mapping
# MTMT file
TESTING_VALID_CUSTOM_ETM_FILE = test_resource_paths.mtmt_mobile_custom_api_example
TESTING_MTMT_INVALID_FILE = test_resource_paths.mtmt_invalid_file


class TestCliEtmErrorCodes:

    @mark.parametrize('default_mapping_file, custom_mapping_file', [
        (TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME, TESTING_MTMT_INVALID_MAPPING_FILENAME),
        (TESTING_MTMT_INVALID_MAPPING_FILENAME, TESTING_MTMT_CUSTOM_VALID_MAPPING_FILENAME),
        (TESTING_MTMT_INVALID_MAPPING_FILENAME, TESTING_MTMT_INVALID_MAPPING_FILENAME)
    ])
    @patch('slp_mtmt.slp_mtmt.mtmt_processor.MTMTProcessor.process')
    def test_etm_mapping_file_not_valid_error(self, mock_load_source_data, default_mapping_file, custom_mapping_file):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = MappingFileNotValidError('Mapping file is not valid', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid MTMT type
                '--etm-type', TESTING_ETM_TYPE,
                #   and a default mapping file
                '--default-mapping-file', default_mapping_file,
                #   and a custom mapping file
                '--custom-mapping-file', custom_mapping_file,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_CUSTOM_ETM_FILE]

            # When parse command of the CLI is called
            result = runner.invoke(parse_any, args)

            # THEN a 22 exit code is returned
            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 22

    @patch('slp_mtmt.slp_mtmt.mtmt_processor.MTMTProcessor.process')
    def test_etm_parse_source_file_not_valid_error(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = SourceFileNotValidError('TM file is not valid', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid MTMT type
                '--etm-type', TESTING_ETM_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #  and an invalid MTMT file
                TESTING_MTMT_INVALID_FILE]

            # When parse command of the CLI is called
            result = runner.invoke(parse_any, args)

            # THEN a 52 exit code is returned
            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 52

    @patch('slp_mtmt.slp_mtmt.mtmt_processor.MTMTProcessor.process')
    def test_etm_loading_source_file_error(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = LoadingSourceFileError('Source file cannot be loaded', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid MTMT type
                '--etm-type', TESTING_ETM_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #  and an invalid MTMT file
                TESTING_MTMT_INVALID_FILE]

            # When parse command of the CLI is called
            result = runner.invoke(parse_any, args)

            # THEN a 52 exit code is returned
            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 51
