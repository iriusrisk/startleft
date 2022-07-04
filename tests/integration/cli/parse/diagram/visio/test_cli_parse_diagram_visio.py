from click.testing import CliRunner
from startleft.cli import parse_any
from tests.resources import test_resource_paths
from tests.util.otm import validate_and_diff as validate_and_diff_otm

# mappings
VISIO_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_visio_mapping
VISIO_CUSTOM_VALID_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
# diagrams
VISIO_DIAGRAM_AWS_SHAPES = test_resource_paths.visio_aws_shapes
VISIO_DIAGRAM_AWS_STENCILS = test_resource_paths.visio_aws_stencils
VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC = test_resource_paths.visio_aws_with_tz_and_vpc
VISIO_ORPHAN_DATAFLOWS = test_resource_paths.visio_orphan_dataflows
# otm
OTM_AWS_SHAPES_EXPECTED = test_resource_paths.visio_aws_shapes_otm_expected
OTM_AWS_WITH_TZ_AND_VPC = test_resource_paths.visio_aws_with_tz_and_vpc_otm_expected
OTM_ORPHAN_DATAFLOWS = test_resource_paths.visio_orphan_dataflows_otm_expected
# the excluded regex for otm diff
excluded_regex = r"root\[\'dataflows'\]\[.+?\]\['name'\]"


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
                '--diagram-type', "VISIO",
                #   and a valid mapping visio default file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "test_parse_diagram_file_ok",
                #   and a valid project id
                '--project-id', "test_parse_diagram_file_ok",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_SHAPES]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff_otm(output_file_name, OTM_AWS_SHAPES_EXPECTED, excluded_regex) == {}

    def test_parse_diagram_with_custom_mapping_file_ok(self):
        """
        Parse Visio file with default and custom mapping files
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping visio default file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid custom mapping visio default file
                '--custom-mapping-file', VISIO_CUSTOM_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "test_parse_diagram_file_ok",
                #   and a valid project id
                '--project-id', "test_parse_diagram_file_ok",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff_otm(output_file_name, OTM_AWS_WITH_TZ_AND_VPC, excluded_regex) == {}

    def test_parse_diagram_with_orphan_dataflows(self):
        """
        Parse Visio file with orphan dataflows
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', "VISIO",
                #   and a valid mapping visio default file
                '--default-mapping-file', VISIO_DEFAULT_VALID_MAPPING_FILENAME,
                #   and a valid project name
                '--project-name', "project-name",
                #   and a valid project id
                '--project-id', "project-id",
                #   and a valid output file name
                '--output-file', output_file_name,
                #   and a valid input file
                VISIO_ORPHAN_DATAFLOWS]

            # When parsing
            result = runner.invoke(parse_any, args)

            # Then validator OTM file is generated
            assert result.exit_code == 0
            # and validate and compare otm files
            assert validate_and_diff_otm(output_file_name, OTM_ORPHAN_DATAFLOWS, excluded_regex) == {}
