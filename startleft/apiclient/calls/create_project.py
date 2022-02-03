import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class CreateProject(BaseApiClient):

    def do_call(self, otm_file):
        logger.debug("Creating project")

        url = self.irius_v1_url(f"/products/otm")
        headers = self.headers()
        files = self.open_file(otm_file)

        response = requests.post(url, headers=headers, files=files)
        self.check_response(response)
        response.close()
