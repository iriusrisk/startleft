import pytest
from click.testing import CliRunner
from startleft.tests.resources.test_resource_paths import invalid_mapping_file_vsdx, invalid_mapping_zip, \
    invalid_mapping_pdf
from startleft.startleft.cli.cli import validate


class TestCliValidate:
    @pytest.mark.parametrize('provider_type, mapping_file', [
        pytest.param("CLOUDFORMATION", invalid_mapping_file_vsdx, id="with invalid iac vsdx mapping file"),
        pytest.param("TERRAFORM", invalid_mapping_zip, id="with invalid iac zip mapping file"),
        pytest.param("CLOUDFORMATION", invalid_mapping_pdf, id="with invalid iac pdf mapping file"),
        pytest.param("VISIO", invalid_mapping_file_vsdx, id="with invalid diagram vsdx mapping file"),
        pytest.param("VISIO", invalid_mapping_zip, id="with invalid diagram zip mapping file"),
        pytest.param("VISIO", invalid_mapping_pdf, id="with invalid diagram pdf mapping file")])
    def test_validate_invalid_mapping_file_error(self, provider_type, mapping_file):
        """
        Validating mapping files with invalid files
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # the provider type
                '--mapping-type', provider_type,
                # the mapping file type and the file to test
                '--mapping-file', mapping_file
            ]

            # When validating
            result = runner.invoke(validate, args)

            # Then a MappingFileNotValidError is raised
            assert result.exit_code == 1
            assert result.exception.error_code.name == 'MAPPING_FILE_NOT_VALID'

            # AND the exit code is 22
            assert result.exception.error_code.system_exit_status == 22


    @pytest.mark.parametrize('file', [
        pytest.param(invalid_mapping_file_vsdx, id="with invalid diagram vsdx mapping file"),
        pytest.param(invalid_mapping_zip, id="with invalid diagram zip mapping file"),
        pytest.param(invalid_mapping_pdf, id="with invalid diagram pdf mapping file")])
    def test_validate_invalid_otm_file_error(self, file):
        """
        Validating mapping files with invalid files
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # the file type and the file to test
                '--otm-file', file]

            # When validating
            result = runner.invoke(validate, args)

            # Then a OtmResultError is raised
            assert result.exit_code == 1
            assert result.exception.error_code.name == 'OTM_RESULT_ERROR'

            # AND the exit code is 42
            assert result.exception.error_code.system_exit_status == 42

