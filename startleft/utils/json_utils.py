# TODO this utils file should be renamed to otm_utils

import json
import logging

from startleft.api.errors import OtmGenerationError
from startleft.otm.otm import OTM

logger = logging.getLogger(__name__)


def get_otm_as_json(otm: OTM):
    logger.info("getting OTM contents as JSON")
    return json.dumps(otm.json(), indent=2)


def get_otm_as_file(otm: OTM, out_file: str):
    logger.info(f"Writing OTM file to '{out_file}'")
    try:
        with open(out_file, "w") as f:
            json.dump(otm.json(), f, indent=2)
    except Exception as e:
        logger.error(f"Unable to create the threat model: {e}")
        raise OtmGenerationError("Unable to create the OTM", e.__class__.__name__, str(e.__cause__))
