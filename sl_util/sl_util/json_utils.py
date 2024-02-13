import json
import logging
from typing import Union

import yaml

from otm.otm.entity.otm import OTM
from sl_util.sl_util.file_utils import read_byte_data

logger = logging.getLogger(__name__)


def __yaml_data_as_str(data: Union[str, bytes]) -> str:
    return data if isinstance(data, str) else read_byte_data(data)


def get_otm_as_json(otm: OTM):
    logger.info("getting OTM contents as JSON")
    return json.dumps(otm.json(), indent=2)


def read_yaml(data: bytes, loader=yaml.SafeLoader) -> dict:
    return yaml.load(__yaml_data_as_str(data), Loader=loader)


def read_json(data: bytes) -> dict:
    return json.loads(__yaml_data_as_str(data))
