import random
from typing import List

import pytest
from pytest import mark, param, fixture

from slp_base import IacFileNotValidError
from slp_tfplan.slp_tfplan.validate.tfplan_validator import TFPlanValidator
from sl_util.sl_util.str_utils import get_bytes

MINIMUM_VALID_TFPLAN_SOURCE = get_bytes('{"planned_values":{"root_module":{"resources":[]}},"configuration":{}}',
                                        'utf-8')
MINIMUM_VALID_TFGRAPH_SOURCE = get_bytes('digraph {subgraph "root" {}}', 'utf-8')

TFPLAN_VALID_MIME = 'application/json'
TFGRAPH_VALID_MIME = 'text/plain'
VALID_MIME_TYPES = [TFPLAN_VALID_MIME, TFGRAPH_VALID_MIME]

MIN_FILE_SIZE = 20
MAX_TFPLAN_FILE_SIZE = 5 * 1024 * 1024
MAX_TFGRAPH_FILE_SIZE = 2 * 1024 * 1024


def create_artificial_file(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


@fixture(autouse=True)
def mocked_mime_types():
    yield VALID_MIME_TYPES


@fixture
def mock_mime_checker(mocker, mocked_mime_types):
    mocker.patch('magic.Magic.from_buffer', side_effect=mocked_mime_types)


class TestTFPlanValidator:

    def test_valid_tfplan_and_tfgraph(self):
        # GIVEN a valid tfplan
        tfplan = MINIMUM_VALID_TFPLAN_SOURCE

        # AND a valid tfgraph
        tfgraph = MINIMUM_VALID_TFGRAPH_SOURCE

        # WHEN TFPlanValidator::validate is invoked
        TFPlanValidator([tfplan, tfgraph]).validate()

        # THEN no error is raised

    @mark.parametrize('sources', [
        param([], id='no sources'),
        param([MINIMUM_VALID_TFPLAN_SOURCE], id='missing one source'),
        param([MINIMUM_VALID_TFPLAN_SOURCE] * random.randint(3, 10), id='more than two sources'),
    ])
    def test_wrong_number_of_sources(self, sources: List[bytes]):
        # GIVEN a wrong number of sources

        # WHEN TFPlanValidator::validate is invoked
        # THEN a IacFileNotValidError is raised
        with pytest.raises(IacFileNotValidError) as error:
            TFPlanValidator(sources).validate()

        # AND whose information is right
        assert error.value.title == 'Wrong number of files'
        assert error.value.message == 'Required one tfplan and one tfgraph files'

    def test_two_tfplan(self):
        # GIVEN two tfplan files
        sources = [MINIMUM_VALID_TFPLAN_SOURCE, MINIMUM_VALID_TFPLAN_SOURCE]

        # WHEN TFPlanValidator::validate is invoked
        # THEN a IacFileNotValidError is raised
        with pytest.raises(IacFileNotValidError) as error:
            TFPlanValidator(sources).validate()

        # AND whose information is right
        assert error.value.title == 'Two tfplan files'
        assert error.value.message == 'Required one tfplan and one tfgraph files'

    @mark.usefixtures('mock_mime_checker')
    @mark.parametrize('sources', [
        param([create_artificial_file(MIN_FILE_SIZE - 1), MINIMUM_VALID_TFGRAPH_SOURCE], id='tfplan too small'),
        param([create_artificial_file(MAX_TFPLAN_FILE_SIZE + 1), MINIMUM_VALID_TFGRAPH_SOURCE], id='tfplan too big'),
        param([MINIMUM_VALID_TFPLAN_SOURCE, create_artificial_file(MIN_FILE_SIZE - 1)], id='tfgraph too small'),
        param([MINIMUM_VALID_TFPLAN_SOURCE, create_artificial_file(MAX_TFGRAPH_FILE_SIZE + 1)], id='tfgraph too big')
    ])
    def test_invalid_size(self, sources: List[bytes]):
        # GIVEN a tfplan with an invalid size

        # WHEN TFPlanValidator::validate is invoked
        # THEN a IacFileNotValidError is raised
        with pytest.raises(IacFileNotValidError) as error:
            TFPlanValidator(sources).validate()

        # AND whose information is right
        assert error.value.title == 'Terraform Plan file is not valid'
        assert error.value.message == 'Provided iac_file is not valid. Invalid size'

    @mark.usefixtures('mock_mime_checker')
    @mark.parametrize('mocked_mime_types', [
        param(['text/xml', 'text/plain'], id='tfplan wrong'),
        param(['application/json', 'text/xml'], id='tfgraph wrong'),
        param(['text/xml', 'text/xml'], id='both wrong')
    ])
    def test_invalid_file_type(self, mocked_mime_types: List[str]):
        # GIVEN a tfplan with an invalid size
        mocked_sources = [create_artificial_file(len(MINIMUM_VALID_TFPLAN_SOURCE)),
                          create_artificial_file(len(MINIMUM_VALID_TFGRAPH_SOURCE))]

        # WHEN TFPlanValidator::validate is invoked
        # THEN a IacFileNotValidError is raised
        with pytest.raises(IacFileNotValidError) as error:
            TFPlanValidator(mocked_sources).validate()

        # AND whose information is right
        assert error.value.title == 'Terraform Plan file is not valid'
        assert error.value.message == 'Invalid content type for iac_file'

    def test_tfplan_wrong_schema(self):
        # GIVEN a valid tfgraph
        tfgraph = MINIMUM_VALID_TFGRAPH_SOURCE

        # AND an invalid tfplan
        tfplan = bytes('{"invalid": "tfplan"}', 'utf-8')

        # WHEN TFPlanValidator::validate is invoked
        # THEN a IacFileNotValidError is raised
        with pytest.raises(IacFileNotValidError) as error:
            TFPlanValidator([tfplan, tfgraph]).validate()

        # AND whose information is right
        assert error.value.title == 'Terraform Plan file is not valid'
        assert error.value.message == 'Invalid content type for iac_file'
