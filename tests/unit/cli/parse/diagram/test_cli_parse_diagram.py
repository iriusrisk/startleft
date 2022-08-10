import logging
from unittest.mock import patch

from click.testing import CliRunner

# mappings
from startleft.cli import parse_any
from tests.resources import test_resource_paths

VISIO_DEFAULT_VALID_MAPPING_FILENAME = test_resource_paths.default_visio_mapping
VISIO_CUSTOM_VALID_MAPPING_FILENAME = test_resource_paths.custom_vpc_mapping
# diagrams
VISIO_DIAGRAM_AWS_WITH_TZ_AND_VPC = test_resource_paths.visio_aws_with_tz_and_vpc


class TestCliParseDiagram:

    @patch('startleft.cli.parse_diagram')
    def test_parse_diagram_file_ok(self, mock, caplog):
        """
        Parsing Cloudformation file wih a valid mapping file
        """
        runner = CliRunner()
        output_file_name = "output-file.otm"
        caplog.set_level(logging.INFO)

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

            # Then validator OTM file is generated
            assert result.exit_code == 0
            assert 'Parsing source files into OTM' in caplog.text
            mock.assert_called_once()
