import logging

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class UpdateProject(BaseApiClient):

    def do_call(self, project_id: str, otm_file):
        logger.debug("Updating project")

        self.put(f"/products/otm/{project_id}", self._build_token_header(), otm_file)
