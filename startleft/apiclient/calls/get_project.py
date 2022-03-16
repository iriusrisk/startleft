import logging

import requests

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class GetProject(BaseApiClient):
    def do_call(self, project_id: str):
        logger.info(f"Getting project with id '{project_id}'")

        return self.get(f"/products/{project_id}", self._build_token_header())
