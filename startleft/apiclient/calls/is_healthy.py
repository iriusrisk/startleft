import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class IsHealthy(BaseApiClient):

    def do_call(self) -> bool:
        logger.debug("Checking is healthy")

        try:
            url = self.base_url + "/health"
            response = requests.get(url)
            return response.status_code == 200
        except ConnectionError:
            return False
