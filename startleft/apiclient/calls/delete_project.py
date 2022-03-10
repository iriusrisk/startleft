import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class DeleteProject(BaseApiClient):

    def do_call(self, project_id: str):
        logger.debug("Deleting project")

        url = self.irius_v1_url(f"/products/{project_id}")
        headers = self.headers()
        response = requests.delete(url, headers=headers)
        self.check_response(response)
        response.close()
