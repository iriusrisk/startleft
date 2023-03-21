import pytest
from pytest import mark, param

from slp_base import LoadingIacFileError
from slp_tf.tests.utility import excluded_regex
from sl_util.sl_util.file_utils import get_byte_data
from slp_tf import TerraformProcessor
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping, \
    tfplan_elb_expected, tfplan_elb, terraform_elb, tfplan_graph_elb, tfplan_sgs, \
    tfplan_graph_sgs, tfplan_graph_sgs_expected, tfplan_graph_elb_expected, tfplan_graph_official_expected, \
    tfplan_official, tfplan_graph_official
from slp_base.tests.util.otm import validate_and_compare

DEFAULT_MAPPING_FILE = terraform_iriusrisk_tf_aws_mapping
SAMPLE_VALID_TFPLAN = get_byte_data(tfplan_elb)
SAMPLE_VALID_TF = get_byte_data(terraform_elb)
SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTfplan:

    @mark.parametrize('tfplan,expected',
                      [param(get_byte_data(tfplan_elb), tfplan_elb_expected, id='elb-example')])
    def test_only_tfplan_examples(self, tfplan: bytes, expected: str):
        # GIVEN a valid TFPLAN file
        # AND a valid TF mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # WHEN the TFPLAN file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tfplan], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        left, right = validate_and_compare(otm, expected, excluded_regex)
        assert left == right

    @mark.parametrize('tfplan,tfgraph,expected',
                      [param(get_byte_data(tfplan_elb), get_byte_data(tfplan_graph_elb), tfplan_graph_elb_expected,
                             id='elb-example'),
                       param(get_byte_data(tfplan_sgs), get_byte_data(tfplan_graph_sgs), tfplan_graph_sgs_expected,
                             id='sgs-example'),
                       param(get_byte_data(tfplan_official), get_byte_data(tfplan_graph_official),
                             tfplan_graph_official_expected,
                            id='official-example')])
    def test_tfplan_tfgraph_examples(self, tfplan: bytes, tfgraph: bytes, expected: str):
        # GIVEN a valid TFPLAN file
        # AND a valid TF mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # WHEN the TFPLAN file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tfplan, tfgraph], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        left, right = validate_and_compare(otm, expected, excluded_regex)
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
        assert str(error.value.message) == 'Only one Terraform plan and an optional Terraform graph supported'

    def test_mixed_tfplan_tfconfig(self):
        # GIVEN a valid TFPLAN and a valid TF FILE
        sources = [SAMPLE_VALID_TFPLAN, SAMPLE_VALID_TF]

        # WHEN the TFPLAN file is processed
        # THEN a LoadingIacFileError exception is raised
        with pytest.raises(LoadingIacFileError) as error:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

        # AND the message says that no multiple tfplan files can be processed at the same time
        assert str(error.value.title) == 'Mixed Terraform sources'
        assert str(error.value.message) == 'Terraform config files mixed with Terraform plan or graph are not supported'
