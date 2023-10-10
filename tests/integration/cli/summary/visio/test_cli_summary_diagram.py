import os

import pytest
from click.testing import CliRunner

from sl_util.sl_util.file_utils import load_csv_into_dict
from startleft.startleft.cli.cli import summary
from tests.resources import test_resource_paths


class TestCliSummaryDiagram:

    @pytest.mark.parametrize('diagram_type, source_files, default_mapping_file, custom_mapping_file, output_file', [
        pytest.param('VISIO', test_resource_paths.visio_aws_stencils, None, None, None, id='visio by name'),
        pytest.param('LUCID', test_resource_paths.lucid_aws_with_tz, None, None, None, id='lucid by name'),
        pytest.param('LUCID', test_resource_paths.lucid_aws_with_tz, None, None, 'custom-output-file.csv',
                     id='lucid by name with output_file'),
        pytest.param('LUCID', test_resource_paths.lucid_aws_vsdx_folder, None, None, None, id='lucid by folder'),
        pytest.param('LUCID', test_resource_paths.lucid_aws_with_tz, test_resource_paths.default_lucid_mapping, None,
                     None, id='lucid by name with default mapping'),
        pytest.param('LUCID', test_resource_paths.lucid_aws_with_tz, test_resource_paths.default_lucid_mapping,
                     test_resource_paths.lucid_aws_with_tz_mapping, None,
                     id='lucid by name with default and custom mapping'),
        ])
    def test_summary_works_ok(self, diagram_type, source_files, default_mapping_file, custom_mapping_file, output_file):
        """
        Check Summary Diagram works ok
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            # a valid diagram type
            args = ['--diagram-type', diagram_type]

            # an optional default mapping file
            if default_mapping_file:
                args.append('--default-mapping-file')
                args.append(default_mapping_file)

            # an optional custom mapping file
            if custom_mapping_file:
                args.append('--custom-mapping-file')
                args.append(custom_mapping_file)

            # an optional output file
            if output_file:
                args.append('--output-file')
                args.append(output_file)

            # and a valid source file
            args.append(source_files)

            # When summary
            result = runner.invoke(summary, args)

            # Then summary is generated correctly
            assert result.exit_code == 0
            # and the file exists
            assert os.path.isfile(output_file if output_file else 'summary.csv')

    def test_summary_check_csv_content(self):
        """
        Check Summary Diagram csv content
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Given a list of arguments with
            args = [
                # a valid diagram type
                '--diagram-type', 'LUCID',
                # a default mapping file
                '--default-mapping-file', test_resource_paths.default_lucid_mapping,
                # a custom mapping file
                '--custom-mapping-file', test_resource_paths.lucid_aws_with_tz_mapping,
                # and a valid source file
                test_resource_paths.lucid_aws_with_tz,
            ]
            # When summary
            result = runner.invoke(summary, args)
            # Then summary is generated correctly
            assert result.exit_code == 0
            summary_csv = load_csv_into_dict('summary.csv')
            expected_summary_csv = load_csv_into_dict(test_resource_paths.lucid_summary_expected_summary)
            assert expected_summary_csv == summary_csv
