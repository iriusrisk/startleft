from unittest.mock import patch

from click.testing import CliRunner

from startleft.api.errors import OtmGenerationError, LoadingDiagramFileError, DiagramFileNotValidError, \
    MappingFileNotValidError, OtmResultError
from startleft.cli import parse_any
# mappings
from tests.unit.cli.parse.diagram.test_unit_cli_parse_diagram import VISIO_DEFAULT_VALID_MAPPING_FILENAME, \
    VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC


class TestCliDiagramErrorCodes:

    @patch('startleft.otm.otm_project.OtmProject.from_diag_file')
    def test_loadingdiagramfileerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = LoadingDiagramFileError('Diagram file cannot be loaded', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 11

    @patch('startleft.otm.otm_project.OtmProject.from_diag_file')
    def test_diagramfilenotvaliderror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = DiagramFileNotValidError('Diagram file is not valid', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 12

    @patch('startleft.otm.otm_project.OtmProject.from_diag_file')
    def test_mappingfilenotvaliderror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = MappingFileNotValidError('Mapping file is not valid', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 22

    @patch('startleft.otm.otm_project.OtmProject.from_diag_file')
    def test_otmresulterror_code(self, mock_load_source_data):

        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = OtmResultError('Parsing provided given IaC/diagram file with the mapping file provided result in an '
                               'invalid OTM file.', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 42

    @patch('startleft.otm.otm_project.OtmProject.from_diag_file')
    def test_otmgenerationerror_code(self, mock_load_source_data):
        runner = CliRunner()
        output_file_name = "output-file.otm"

        error = OtmGenerationError('Provided files were processed successfully but an error occurred while generating '
                                   'the OTM file.', None, None)

        mock_load_source_data.side_effect = error

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid Diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            assert result.exit_code == 1
            assert result.exception.error_code.system_exit_status == 45

