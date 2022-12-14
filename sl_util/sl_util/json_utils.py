# TODO this utils file should be renamed to otm_utils

import json
import logging

from otm.otm.entity.otm import Otm

logger = logging.getLogger(__name__)


def get_otm_as_json(otm: Otm):
    logger.info("getting OTM contents as JSON")
    return json.dumps(otm.json(), indent=2)



