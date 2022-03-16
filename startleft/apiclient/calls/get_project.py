import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class GetProject(BaseApiClient):
    def do_call(self, project_id: str):
        logger.info(f"Getting project with id '{project_id}'")
        url = self.irius_v1_url(f"/products/{project_id}")
        headers = self.headers()

        logger.debug(f"GET {url} with headers {headers}")
        response = requests.get(url, headers=headers)
        self.check_response(response)

        return response.json()
