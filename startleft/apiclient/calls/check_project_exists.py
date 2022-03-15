import logging
from json.decoder import JSONDecodeError

import requests

from startleft.api.errors import IriusCommonApiError
from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class CheckProjectExists(BaseApiClient):

    def do_call(self, project_id: str) -> bool:
        logger.debug("Checking if project exists")

        response = self.get("/products", self._build_token_header())

        try:
            for project in response.json():
                if project["ref"] == project_id:
                    return True
        except JSONDecodeError:
            raise IriusCommonApiError(http_status_code=500,
                                      message=f"API did not return a JSON response: {response.text}")
        return False
