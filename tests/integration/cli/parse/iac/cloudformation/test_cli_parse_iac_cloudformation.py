from click.testing import CliRunner
from tests.resources import test_resource_paths
from startleft.cli import parse_any
from tests.util.otm import validate_and_diff as validate_and_diff_otm
from tests.integration.cli.parse.iac.test_cli_parse_iac import excluded_regex

# mappings
CLOUDFORMATION_MAPPING = test_resource_paths.default_cloudformation_mapping
# IaC files
CLOUDFORMATION_FOR_MAPPING_TESTS = test_resource_paths.cloudformation_for_mappings_tests_json
CLOUDFORMATION_UNKNOWN_RESOURCE = test_resource_paths.cloudformation_unknown_resource
# otm
OTM_CFT_FOR_MAPPING_TESTS = test_resource_paths.cloudformation_for_mappings_tests_json_otm_expected
OTM_EMPTY_FILE = test_resource_paths.otm_empty_file_example


class TestCliParseIaCCloudformation:
    """
    The testing for click parse commands for CLOUDFORMATION files
    """

    def test_parse_cloudformation_file_ok(self):
        """
        Parsing Cloudformation file wih a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

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
            # and validate and compare otm files
            validate_and_diff_otm(output_file_name, OTM_CFT_FOR_MAPPING_TESTS, excluded_regex)

    def test_parse_cloudformation_unknown_resources(self):
        """
        Parsing Cloudformation file wih unknown resources
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

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
                CLOUDFORMATION_UNKNOWN_RESOURCE]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            validate_and_diff_otm(output_file_name, OTM_EMPTY_FILE, excluded_regex)