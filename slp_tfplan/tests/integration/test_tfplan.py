import random
from typing import List

import pytest
from pytest import mark, param

import slp_tfplan.tests.resources.test_resource_paths as resources
from otm.otm.entity.otm import OTM
from sl_util.sl_util.file_utils import get_byte_data
from slp_base import IacFileNotValidError
from slp_base.tests.util.otm import validate_and_compare
from slp_tfplan import TFPlanProcessor
from slp_tfplan.tests.util.builders import create_artificial_file, MIN_FILE_SIZE, MAX_TFPLAN_FILE_SIZE, \
    MAX_TFGRAPH_FILE_SIZE

DEFAULT_MAPPING_FILE = get_byte_data(resources.terraform_iriusrisk_tfplan_aws_mapping)

SAMPLE_VALID_TFPLAN = get_byte_data(resources.tfplan_elb)
SAMPLE_VALID_TFGRAPH = get_byte_data(resources.tfgraph_elb)

SAMPLE_INVALID_TFPLAN = get_byte_data(resources.invalid_yaml)
SAMPLE_INVALID_TFGRAPH = get_byte_data(resources.invalid_yaml)

TFPLAN_OFFICIAL = get_byte_data(resources.tfplan_official)
TFGRAPH_OFFICIAL = get_byte_data(resources.tfgraph_official)

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
EXCLUDED_REGEX = r"root\[\'dataflows'\]\[.+?\]\['id'\]"


def __extract_and_order_components(otm: OTM):
    return sorted(otm.components, key=lambda x: x.id)

@mark.parametrize('tfplan,tfgraph,expected',
                  [param(get_byte_data(resources.tfplan_elb), get_byte_data(resources.tfgraph_elb), resources.otm_expected_elb,
                         id='elb-example'),
                   param(get_byte_data(resources.tfplan_sgs), get_byte_data(resources.tfgraph_sgs), resources.otm_expected_sgs,
                         id='sgs-example'),
                   param(get_byte_data(resources.tfplan_official), get_byte_data(resources.tfgraph_official),
                         resources.otm_expected_official,
                         id='official-example')])
def test_tfplan_tfgraph_examples(tfplan: bytes, tfgraph: bytes, expected: str):
    # GIVEN a valid TFPLAN file and a valid tfgraph
    # AND a valid TF mapping file
    mapping_file = DEFAULT_MAPPING_FILE

    # WHEN TFPlanProcessor::process is invoked
    otm = TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, [tfplan, tfgraph], [mapping_file]).process()

    # THEN the resulting OTM match the expected one
    left, right = validate_and_compare(otm, expected, EXCLUDED_REGEX)
    assert left == right

@mark.parametrize('sources', [
    param([], id='no sources'),
    param([SAMPLE_VALID_TFPLAN], id='one source'),
    param([SAMPLE_VALID_TFPLAN] * random.randint(3, 10), id='more than two sources')
])
def test_wrong_number_of_parameters(sources: List[bytes]):
    # GIVEN a wrong number of sources

    # WHEN TFPlanProcessor::process is invoked
    # THEN a LoadingIacFileError exception is raised
    with pytest.raises(IacFileNotValidError) as error:
        TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

    # AND the message says that the number of parameters is wrong
    assert str(error.value.title) == 'Wrong number of files'
    assert str(error.value.message) == 'Required one tfplan and one tfgraph files'

@mark.parametrize('sources', [
    param([create_artificial_file(MIN_FILE_SIZE - 1), SAMPLE_VALID_TFGRAPH], id='tfplan too small'),
    param([create_artificial_file(MAX_TFPLAN_FILE_SIZE + 1), SAMPLE_VALID_TFGRAPH], id='tfplan too big'),
    param([SAMPLE_VALID_TFPLAN, create_artificial_file(MIN_FILE_SIZE - 1)], id='tfgraph too small'),
    param([SAMPLE_VALID_TFPLAN, create_artificial_file(MAX_TFGRAPH_FILE_SIZE + 1)], id='tfgraph too big')
])
def test_invalid_size(sources: List[bytes]):
    # GIVEN a tfplan or tfgraph with an invalid size

    # WHEN TFPlanProcessor::process is invoked
    # THEN a IacFileNotValidError is raised
    with pytest.raises(IacFileNotValidError) as error:
        TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

    # AND whose information is right
    assert error.value.title == 'Terraform Plan file is not valid'
    assert error.value.message == 'Provided iac_file is not valid. Invalid size'

def test_two_tfplan():
    # GIVEN two valid TFPLANs
    sources = [SAMPLE_VALID_TFPLAN, SAMPLE_VALID_TFPLAN]

    # WHEN TFPlanProcessor::process is invoked
    # THEN a LoadingIacFileError exception is raised
    with pytest.raises(IacFileNotValidError) as error:
        TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

    # AND the message says that no multiple tfplan files can be processed at the same time
    assert str(error.value.title) == 'Two tfplan files'
    assert str(error.value.message) == 'Required one tfplan and one tfgraph files'

@mark.parametrize('sources', [
    param([SAMPLE_INVALID_TFPLAN, SAMPLE_VALID_TFGRAPH], id='invalid tfplan'),
    param([SAMPLE_VALID_TFPLAN, SAMPLE_INVALID_TFGRAPH], id='invalid tfgraph'),
    param([SAMPLE_INVALID_TFPLAN, SAMPLE_INVALID_TFGRAPH], id='both invalid')
])
def test_invalid_sources(sources: List[bytes]):
    # GIVEN some invalid tfplan

    # WHEN TFPlanProcessor::process is invoked
    # THEN a LoadingIacFileError exception is raised
    with pytest.raises(IacFileNotValidError) as error:
        TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, sources, [DEFAULT_MAPPING_FILE]).process()

    # AND the message says that no multiple tfplan files can be processed at the same time
    assert str(error.value.title) == 'Terraform Plan file is not valid'
    assert str(error.value.message) == 'Invalid content type for iac_file'

def test_singleton():
    # GIVEN the mapping file with the singleton behaviour
    mapping_file = get_byte_data(resources.terraform_singleton_mapping)

    # WHEN TFPlanProcessor::process is invoked
    otm = TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, [TFPLAN_OFFICIAL, TFGRAPH_OFFICIAL], [mapping_file]).process()

    # THEN the resources are grouped by type
    components = __extract_and_order_components(otm)
    assert len(components) == 1
    # first component is the API GateWay grouped by regex
    assert components[0].id == 'aws_iam_policy.click_loggerlambda_logging_policy'
    assert components[0].name == 'iam (grouped)'
    assert components[0].type == 'iam'

def test_singleton_grouped_by_category():
    # GIVEN the mapping file with the singleton behaviour
    mapping_file = get_byte_data(resources.terraform_group_by_category_mapping)

    # WHEN TFPlanProcessor::process is invoked
    otm = TFPlanProcessor(SAMPLE_ID, SAMPLE_NAME, [TFPLAN_OFFICIAL, TFGRAPH_OFFICIAL], [mapping_file]).process()

    # AND the resources are grouped by category
    components = __extract_and_order_components(otm)
    assert len(components) == 2
    # first component is the API GateWay grouped by regex
    assert components[0].id == 'aws_api_gateway_account.click_logger_api_gateway_account'
    assert components[0].name == 'API Gateway'
    assert components[0].type== 'api-gateway'
    # second component is the CloudWatch Log Group grouped by array
    assert components[1].id == 'aws_cloudwatch_log_group.click_logger_firehose_delivery_stream_log_group'
    assert components[1].name == 'CloudWatch'
    assert components[1].type == 'cloudwatch'
