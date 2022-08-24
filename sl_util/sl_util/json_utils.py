# TODO this utils file should be renamed to otm_utils

import json
import logging

from otm.otm.otm import OTM

logger = logging.getLogger(__name__)


def get_otm_as_json(otm: OTM):
    logger.info("getting OTM contents as JSON")
    return json.dumps(otm.json(), indent=2)



