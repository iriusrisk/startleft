import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class DeleteProject(BaseApiClient):

    def do_call(self, project_id: str):
        logger.debug("Deleting project in IriusRisk")

        self.delete(f"/products/{project_id}", self._build_token_header(),)
