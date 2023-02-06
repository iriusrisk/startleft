import pytest
from pytest import mark, param

from slp_base import LoadingIacFileError
from slp_tf.tests.integration.test_tf_processor import VALIDATION_EXCLUDED_REGEX
from sl_util.sl_util.file_utils import get_data
from slp_tf import TerraformProcessor
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping, \
    expected_elb_tfplan, tfplan_elb, terraform_elb
from slp_base.tests.util.otm import validate_and_compare

DEFAULT_MAPPING_FILE = terraform_iriusrisk_tf_aws_mapping
SAMPLE_VALID_TFPLAN = get_data(tfplan_elb)
SAMPLE_VALID_TF = get_data(terraform_elb)
SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTfplan:

    @mark.parametrize('source,expected',
                      [param(tfplan_elb, expected_elb_tfplan, id='elb-example')])
    def test_valid_examples(self, source: str, expected: str):
        # GIVEN a valid TFPLAN file
        terraform_file = get_data(source)

        # AND a valid TF mapping file
        mapping_file = get_data(DEFAULT_MAPPING_FILE)

        # WHEN the TFPLAN file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        left, right = validate_and_compare(otm, expected, VALIDATION_EXCLUDED_REGEX)
        assert left == right

    def test_multiple_tfplan(self):
        # GIVEN two valid TFPLANs
        sources = [SAMPLE_VALID_TFPLAN, SAMPLE_VALID_TFPLAN]

        # WHEN the TFPLAN file is processed
        # THEN a LoadingIacFileError exception is raised
        with pytest.raises(LoadingIacFileError) as error:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

        # AND the message says that no multiple tfplan files can be processed at the same time
        assert str(error.value.title) == 'Multiple Terraform plan files'
        assert str(error.value.message) == 'Multiple Terraform plan files cannot be loaded at the same time.'

    def test_mixed_tfplan_tfconfig(self):
        # GIVEN a valid TFPLAN and a valid TF FILE
        sources = [SAMPLE_VALID_TFPLAN, SAMPLE_VALID_TF]

        # WHEN the TFPLAN file is processed
        # THEN a LoadingIacFileError exception is raised
        with pytest.raises(LoadingIacFileError) as error:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

        # AND the message says that no multiple tfplan files can be processed at the same time
        assert str(error.value.title) == 'Mixed Terraform files'
        assert str(error.value.message) == 'Terraform Config and Plan files cannot be loaded at the same time.'
