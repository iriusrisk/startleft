from unittest.mock import patch

from click.testing import CliRunner

from slp_base import LoadingMappingFileError, LoadingIacFileError, IacFileNotValidError, \
    OTMBuildingError, \
    OTMGenerationError
from startleft.startleft.cli.cli import parse_any
from startleft.tests.unit.cli.parse.iac.test_unit_cli_parse_iac import CLOUDFORMATION_MAPPING, \
    CLOUDFORMATION_FOR_MAPPING_TESTS

TESTING_IAC_TYPE = 'CLOUDFORMATION'
TESTING_IAC_FILE = CLOUDFORMATION_FOR_MAPPING_TESTS
TESTING_MAPPING_FILE = CLOUDFORMATION_MAPPING


class TestCliIacErrorCodes:

    @patch('slp_base.slp_base.otm_processor.OTMProcessor.process')
    def test_loadingiacfilerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = LoadingIacFileError('IaC file cannot be loaded', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_IAC_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_MAPPING_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 1

    @patch('slp_base.slp_base.otm_processor.OTMProcessor.process')
    def test_iacfilenotvaliderror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = IacFileNotValidError('IaC file is not valid', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_IAC_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_MAPPING_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 2

    @patch('slp_base.slp_base.otm_processor.OTMProcessor.process')
    def test_loadingmappingfileerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = LoadingMappingFileError('Mapping file cannot be loaded', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_IAC_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_MAPPING_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 21

    @patch('slp_base.slp_base.otm_processor.OTMProcessor.process')
    def test_otmbuildingerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = OTMBuildingError('Error during OTM transformation. Eg: bad jmespath expression.', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_IAC_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_MAPPING_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 41

    @patch('slp_base.slp_base.otm_processor.OTMProcessor.process')
    def test_otmgenerationerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = OTMGenerationError('Provided files were processed successfully but an error occurred while generating'
                                   ' the OTM file.', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid IaC type
                '--iac-type', TESTING_IAC_TYPE,
                #   and a valid mapping file
                '--default-mapping-file', TESTING_IAC_FILE,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_MAPPING_FILE]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 45
