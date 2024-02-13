import json
import logging

import yaml

from otm.otm.entity.otm import OTM
from sl_util.sl_util.file_utils import read_byte_data

logger = logging.getLogger(__name__)


def get_otm_as_json(otm: OTM):
    logger.info("getting OTM contents as JSON")
    return json.dumps(otm.json(), indent=2)


def yaml_data_as_str(data) -> str:
    return data if isinstance(data, str) else read_byte_data(data)


def yaml_reader(data, loader=yaml.BaseLoader):
    return yaml.load(yaml_data_as_str(data), Loader=loader)
