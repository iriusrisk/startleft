import logging

from click.testing import CliRunner

from startleft.startleft.cli.cli import validate
from tests.resources import test_resource_paths

SAMPLE_OTM_FILENAME = test_resource_paths.otm_file_example
SAMPLE_OTM_YAML_FILENAME = test_resource_paths.otm_yaml_file_example
IAC_VALID_MAPPING_FILENAME = test_resource_paths.default_cloudformation_mapping
INVALID_YAML_FILENAME = test_resource_paths.invalid_yaml
CUSTOM_YAML_VISIO_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
MTMT_MAPPING_FILENAME_VALID = test_resource_paths.mtmt_mapping_file_valid
MTMT_MAPPING_FILENAME_INVALID = test_resource_paths.mtmt_mapping_file_invalid


class TestCliValidate:
    """
    The testing for click validate commands
    """
    def test_validate_otm_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a valid OTM file
        result = runner.invoke(validate, ['--otm-file', SAMPLE_OTM_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating OTM is performed
        assert 'Validating OTM file' in caplog.text
        #   and validation OTM finish successfully
        assert 'OTM file validated successfully' in caplog.text

    def test_validate_otm_yaml_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a valid OTM file in YAML format
        result = runner.invoke(validate, ['--otm-file', SAMPLE_OTM_YAML_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating OTM is performed
        assert 'Validating OTM file' in caplog.text
        #   and validation OTM finish successfully
        assert 'OTM file validated successfully' in caplog.text

    def test_validate_iac_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a valid IaC mapping file
        result = runner.invoke(validate, ['--iac-mapping-file', IAC_VALID_MAPPING_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating IaC is performed
        assert 'Validating IaC mapping files' in caplog.text
        #   and validation IaC finish successfully
        assert 'Mapping files are valid' in caplog.text

    def test_validate_diagram_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating a Diagram mapping file
        result = runner.invoke(validate, ['--diagram-mapping-file', CUSTOM_YAML_VISIO_MAPPING_FILENAME])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating Diagram is performed
        assert 'Validating Diagram mapping files' in caplog.text
        #   and validation Diagram finish successfully
        assert 'Mapping files are valid' in caplog.text

    def test_validate_valid_etm_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating an External Threat Model mapping file
        result = runner.invoke(validate, ['--etm-mapping-file', MTMT_MAPPING_FILENAME_VALID])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validation ETM is performed
        assert 'Validating External Threat Model mapping files' in caplog.text
        #   and validation ETM finish successfully
        assert 'Mapping files are valid' in caplog.text

    def test_validate_invalid_etm_file(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating an External Threat Model mapping file
        result = runner.invoke(validate, ['--etm-mapping-file', MTMT_MAPPING_FILENAME_INVALID])

        # Then validator returns not OK
        assert result.exit_code == 1
        #   and validation ETM is performed
        assert 'Validating External Threat Model mapping files' in caplog.text
        #   and validation ETM finish unsuccessfully
        assert 'Mapping file is not valid' in caplog.text
        assert '\'label\' is a required property' in caplog.text

    def test_validate_multiple_files(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # When validating multiple files
        result = runner.invoke(validate, [
            '--otm-file', SAMPLE_OTM_FILENAME,
            '--iac-mapping-file', IAC_VALID_MAPPING_FILENAME,
            '--diagram-mapping-file', CUSTOM_YAML_VISIO_MAPPING_FILENAME
        ])

        # Then validator returns OK
        assert result.exit_code == 0
        #   and validating OTM file is performed
        assert 'Validating OTM file' in caplog.text
        #   and validation OTM finish successfully
        assert 'OTM file validated successfully' in caplog.text
        #   and validating IaC is performed
        assert 'Validating IaC mapping files' in caplog.text
        #   and validation IaC finish successfully
        assert 'Mapping files are valid' in caplog.text
        #   and validating Diagram is performed
        assert 'Validating Diagram mapping files' in caplog.text
        #   and validation Diagram finish successfully
        assert 'Mapping files are valid' in caplog.text
