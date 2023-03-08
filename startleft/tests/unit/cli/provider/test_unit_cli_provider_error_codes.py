from unittest.mock import patch

from click.testing import CliRunner

from slp_base import ProviderNotFoundError
from startleft.startleft.cli.cli import parse_any
from startleft.tests.resources import test_resource_paths

TESTING_ETM_TYPE = 'MTMT'
# mappings
TESTING_MTMT_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_mtmt_mapping
# MTMT file
TESTING_VALID_CUSTOM_ETM_FILE = test_resource_paths.mtmt_mobile_custom_api_example


class TestCliProviderResolverErrorCode:

    # This test check the exit status code if there is not any provider found the processor is irrelevant here, it used
    # to run the CliRunner.
    @patch('slp_mtmt.slp_mtmt.mtmt_processor.MTMTProcessor.process')
    def test_etm_loading_source_file_error(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = ProviderNotFoundError('Source file cannot be loaded', None, None)

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
                TESTING_VALID_CUSTOM_ETM_FILE]

            # When parse command of the CLI is called
            result = runner.invoke(parse_any, args)

            # THEN a 60 exit code is returned
            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 60
