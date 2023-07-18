import json
import logging
from json import JSONDecodeError
from typing import List, Dict

import sl_util.sl_util.secure_regex as re
from sl_util.sl_util.file_utils import get_file_type_by_content, read_byte_data
from slp_base import IacFileNotValidError, IacType
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.provider_validator import generate_size_error, generate_content_type_error
from slp_base.slp_base.schema import Schema

logger = logging.getLogger(__name__)

MIN_FILE_SIZE = 20
MAX_TFPLAN_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_TFGRAPH_FILE_SIZE = 2 * 1024 * 1024  # 2MB

TFPLAN_MIME_TYPE = 'application/json'
TFGRAPH_MIME_TYPE = 'text/plain'

TFPLAN_SCHEMA_FILENAME = 'tfplan_schema.json'
VALID_TFGRAPH_REGEX = r"\bdigraph[\s\S]*\bsubgraph[\s\S]*"


def is_valid_tfplan(tfplan: bytes) -> bool:
    schema = Schema.from_package('slp_tfplan', TFPLAN_SCHEMA_FILENAME)
    try:
        schema.validate(json.loads(tfplan))
    except JSONDecodeError:
        return False

    return schema.valid


def is_valid_tfgraph(tfgraph: bytes) -> bool:
    return bool(re.match(VALID_TFGRAPH_REGEX, read_byte_data(tfgraph)))


class TFPlanValidator(ProviderValidator):

    def __init__(self, sources: List[bytes]):
        super(TFPlanValidator, self).__init__()
        self.sources = sources

        self.param_sources: Dict[str, bytes] = {}

    def validate(self):
        logger.info('Validating Terraform Plan file')
        self.__validate_number_of_sources()
        self.__validate_request_size()
        self.__validate_file_types()

        self.__match_params_and_sources()
        self.__validate_file_sizes()
        self.__validate_tfgraph()

    def __validate_number_of_sources(self):
        if len(self.sources) != 2:
            raise IacFileNotValidError(
                title='Wrong number of files',
                message='Required one tfplan and one tfgraph files')

    def __validate_request_size(self):
        max_supported_file_size = max(MAX_TFPLAN_FILE_SIZE, MAX_TFGRAPH_FILE_SIZE)
        if len(self.sources[0]) > max_supported_file_size or len(self.sources[0]) < MIN_FILE_SIZE \
                or len(self.sources[1]) > max_supported_file_size or len(self.sources[1]) < MIN_FILE_SIZE:
            raise generate_size_error(IacType.TFPLAN, 'iac_file', IacFileNotValidError)

    def __validate_file_types(self):
        source_types = {get_file_type_by_content((self.sources[0])), get_file_type_by_content((self.sources[1]))}

        if source_types.intersection(IacType.TFPLAN.valid_mime) != source_types:
            raise generate_content_type_error(IacType.TFPLAN, 'iac_file', IacFileNotValidError)

    def __match_params_and_sources(self):
        is_first_source_tfplan = is_valid_tfplan(self.sources[0])
        is_second_source_tfplan = is_valid_tfplan(self.sources[1])

        if is_first_source_tfplan and is_second_source_tfplan:
            raise IacFileNotValidError(
                title='Two tfplan files',
                message='Required one tfplan and one tfgraph files'
            )

        if is_first_source_tfplan == is_second_source_tfplan:
            raise generate_content_type_error(IacType.TFPLAN, 'iac_file', IacFileNotValidError)

        self.param_sources = {
            'tfplan': self.sources[0] if is_first_source_tfplan else self.sources[1],
            'tfgraph': self.sources[0] if is_second_source_tfplan else self.sources[1]
        }

    def __validate_file_sizes(self):
        if len(self.param_sources['tfplan']) > MAX_TFPLAN_FILE_SIZE or \
                len(self.param_sources['tfgraph']) > MAX_TFGRAPH_FILE_SIZE:
            raise generate_size_error(IacType.TFPLAN, 'iac_file', IacFileNotValidError)

    def __validate_tfgraph(self):
        if not is_valid_tfgraph(self.param_sources['tfgraph']):
            raise generate_content_type_error(IacType.TFPLAN, 'iac_file', IacFileNotValidError)
