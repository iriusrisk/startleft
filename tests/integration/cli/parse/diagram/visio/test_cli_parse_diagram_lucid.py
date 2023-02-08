from click.testing import CliRunner
from pytest import mark

from slp_base.slp_base.errors import MappingFileNotValidError, DiagramFileNotValidError
from slp_base.tests.util.otm import validate_and_compare
from startleft.startleft.cli.cli import parse_any
from tests.resources import test_resource_paths

# mappings
LUCID_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_lucid_mapping
TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_FILENAME = test_resource_paths.lucid_aws_with_tz_mapping
TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_AND_VPC_FILENAME = test_resource_paths.lucid_aws_with_tz_and_vpc_mapping
INVALID_YAML = test_resource_paths.invalid_yaml
# diagrams
TESTING_VALID_LUCID_FILE_WITH_TZ = test_resource_paths.lucid_aws_with_tz
TESTING_VALID_LUCID_FILE_WITH_TZ_AND_VPC = test_resource_paths.lucid_aws_with_tz_and_vpc
VISIO_INVALID_FILE_SIZE = test_resource_paths.visio_invalid_file_size
VISIO_INVALID_FILE_TYPE = test_resource_paths.visio_invalid_file_type
# otm
OTM_AWS_WITH_TZ_DEFAULT = test_resource_paths.lucid_aws_with_tz_default_otm
OTM_AWS_WITH_TZ = test_resource_paths.lucid_aws_with_tz_otm
OTM_AWS_WITH_TZ_AND_VPC = test_resource_paths.lucid_aws_with_tz_and_vpc_otm
# the excluded regex for otm diff
excluded_regex = r"root\['dataflows'\]\[.+?\]\['name'\]"


class TestCliParseDiagram:
    """
    The testing for click parse commands for Diagram files
    """

    def test_parse_diagram_file_ok(self):
        """
        Parse Visio file with default mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "LUCID",
                #   and a valid mapping lucidchart default file
                '--default-mapping-file', LUCID_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "test_parse_diagram_file_ok",
                #   and a valid project id
                '--project-id', "test_parse_diagram_file_ok",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_LUCID_FILE_WITH_TZ]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            left, right = validate_and_compare(output_file_name, OTM_AWS_WITH_TZ_DEFAULT, excluded_regex)
            assert left == right

    @mark.parametrize('source_file,custom_mapping_file,expected_otm',
                      [(TESTING_VALID_LUCID_FILE_WITH_TZ, TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_FILENAME, OTM_AWS_WITH_TZ),
                       (TESTING_VALID_LUCID_FILE_WITH_TZ_AND_VPC, TESTING_LUCID_CUSTOM_VALID_MAPPING_WITH_TZ_AND_VPC_FILENAME, OTM_AWS_WITH_TZ_AND_VPC)])
    def test_parse_diagram_with_custom_mapping_file_ok(self, source_file, custom_mapping_file, expected_otm):
        """
        Parse Visio file with default and custom mapping files
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "LUCID",
                #   and a valid mapping lucidchart default file
                '--default-mapping-file', LUCID_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid custom mapping lucidchart default file
                '--custom-mapping-file', custom_mapping_file,
                #   and a valid project name
                '--project-name', "test_parse_diagram_file_ok",
                #   and a valid project id
                '--project-id', "test_parse_diagram_file_ok",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                source_file]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            left, right = validate_and_compare(output_file_name, expected_otm, excluded_regex)
            assert left == right

    @mark.parametrize('filename', [VISIO_INVALID_FILE_SIZE, VISIO_INVALID_FILE_TYPE])
    def test_parse_diagram_with_invalid_lucid_file(self, filename):
        """
        Parse a invalid Visio file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "LUCID",
                #   and a valid mapping lucidchart default file
                '--default-mapping-file', LUCID_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                filename]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then a DiagramFileNotValidError is returned
            assert isinstance(result.exception, DiagramFileNotValidError)

    def test_parse_diagram_with_invalid_default_mapping(self):
        """
        Parse with an invalid Default Mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "LUCID",
                #   and a valid mapping lucidchart default file
                '--default-mapping-file', INVALID_YAML,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                TESTING_VALID_LUCID_FILE_WITH_TZ]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then a MappingFileNotValidError is returned
            assert isinstance(result.exception, MappingFileNotValidError)
