import logging

from click.testing import CliRunner
from startleft.cli import search
from tests.resources import test_resource_paths

TF_AWS_SIMPLE_COMPONENTS_FILENAME = test_resource_paths.terraform_aws_simple_components
CTF_FOR_MAPPING_TESTS = test_resource_paths.cloudformation_for_mappings_tests_json


class TestCliSearch:
    """
    The testing for click search commands
    """
    def test_search_tf_find_results(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # and a list of arguments with
        args = [
            # a valid TERRAFORM type
            '--iac-type', "TERRAFORM",
            # and a valid QUERY
            '--query', "resource[].aws_lambda_function",
            # and a valid input file
            TF_AWS_SIMPLE_COMPONENTS_FILENAME]

        # When searching a valid TERRAFORM file
        result = runner.invoke(search, args)

        # Then validator returns OK
        assert result.exit_code == 0
        #   and searching is performed
        assert 'Running JMESPath search query against the IaC file' in caplog.text
        #   and results are found
        assert 'test_lambda' in caplog.text

    def test_search_ctf_find_results(self, caplog):
        # Given a info level of logging
        caplog.set_level(logging.INFO)
        runner = CliRunner()

        # and a list of arguments with
        args = [
            # a valid CLOUDFORMATION type
            '--iac-type', "CLOUDFORMATION",
            # and a valid QUERY
            '--query', "Resources|squash(@)[?Type=='AWS::EC2::VPC']",
            # and a valid input file
            CTF_FOR_MAPPING_TESTS]

        # When searching a valid CLOUDFORMATION file
        result = runner.invoke(search, args)

        # Then validator returns OK
        assert result.exit_code == 0
        #   and searching is performed
        assert 'Running JMESPath search query against the IaC file' in caplog.text
        #   and results are found
        assert '"_key": "CustomVPC"' in caplog.text
